import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.calcite.config.Lex;
import org.apache.calcite.plan.hep.HepPlanner;
import org.apache.calcite.plan.hep.HepProgram;
import org.apache.calcite.plan.hep.HepProgramBuilder;
import org.apache.calcite.rel.RelNode;
import org.apache.calcite.rel.RelRoot;
import org.apache.calcite.rel.rel2sql.RelToSqlConverter;
import org.apache.calcite.rel.rules.CoreRules;
import org.apache.calcite.rel.type.RelDataType;
import org.apache.calcite.rel.type.RelDataTypeFactory;
import org.apache.calcite.schema.impl.AbstractTable;
import org.apache.calcite.sql.SqlDialect;
import org.apache.calcite.sql.SqlNode;
import org.apache.calcite.sql.dialect.MysqlSqlDialect;
import org.apache.calcite.sql.dialect.PostgresqlSqlDialect;
import org.apache.calcite.sql.dialect.SparkSqlDialect;
import org.apache.calcite.sql.parser.SqlParser;
import org.apache.calcite.sql.type.SqlTypeName;
import org.apache.calcite.tools.FrameworkConfig;
import org.apache.calcite.tools.Frameworks;
import org.apache.calcite.tools.Planner;

public final class CalciteHepRecoveryCanary {
    private static final Pattern COLUMN_PATTERN =
            Pattern.compile(
                    "(?is)^([`\"]?)([a-zA-Z_][\\w]*)([`\"]?)\\s+([a-zA-Z]+(?:\\s+[a-zA-Z]+)?)(?:\\s*\\(([^)]*)\\))?.*$");
    private static final Pattern REDUCED_AVG_PATTERN =
            Pattern.compile(
                    "CAST\\(CAST\\(COALESCE\\(SUM\\((.+?)\\), 0\\) AS DECIMAL\\(15, 2\\)\\) / COUNT\\(\\*\\) AS DECIMAL\\(15, 2\\)\\)");

    private CalciteHepRecoveryCanary() {}

    public static void main(String[] args) throws Exception {
        Map<String, String> parsed = parseArgs(args);
        String caseId = requireArg(parsed, "--case-id");
        String engine = requireArg(parsed, "--engine").toLowerCase(Locale.ROOT);
        Path sourceSqlPath = Path.of(requireArg(parsed, "--source-sql"));
        Path ddlPath = Path.of(requireArg(parsed, "--ddl"));
        Path outputSqlPath = Path.of(requireArg(parsed, "--output-sql"));

        if (!Files.isRegularFile(sourceSqlPath)) {
            throw new IllegalArgumentException("source SQL file missing: " + sourceSqlPath);
        }
        if (!Files.isRegularFile(ddlPath)) {
            throw new IllegalArgumentException("DDL file missing: " + ddlPath);
        }

        String sourceSql = Files.readString(sourceSqlPath, StandardCharsets.UTF_8);
        String ddlSql = Files.readString(ddlPath, StandardCharsets.UTF_8);
        if (sourceSql.trim().isEmpty()) {
            throw new IllegalArgumentException("source SQL is empty");
        }
        if (ddlSql.trim().isEmpty()) {
            throw new IllegalArgumentException("DDL is empty");
        }

        runRecoveryCanary(caseId, engine, sourceSql, ddlSql, outputSqlPath);
    }

    private static void runRecoveryCanary(
            String caseId, String engine, String sourceSql, String ddlSql, Path outputSqlPath) throws Exception {
        LinkedHashMap<String, String> result = new LinkedHashMap<>();
        result.put("case_id", caseId);
        result.put("engine", engine);
        result.put("source_sql_accepted", "true");
        result.put("ddl_accepted", "true");
        result.put("schema_ddl_ingestion_succeeded", "false");
        result.put("calcite_parse_succeeded", "false");
        result.put("validation_succeeded", "false");
        result.put("sql_to_rel_succeeded", "false");
        result.put("hep_planner_succeeded", "false");
        result.put("rel_to_sql_succeeded", "false");
        result.put("candidate_sql_emitted", "false");
        result.put("dialect_rendering_status", "target_dialect_unavailable");
        result.put("route_stage_reached", "read_inputs");
        result.put("failure_category", "");
        result.put("blocker_reason", "");
        result.put("rewrite_changed", "");

        SqlDialect dialect = selectDialect(engine);
        Lex parserLex = selectParserLex(engine);
        SqlParser.Config parserConfig = SqlParser.config().withLex(parserLex);
        result.put("dialect_class_used", dialect.getClass().getName());
        result.put("parser_lex_used", parserLex.name());

        String parseCandidateSql = stripTrailingSemicolon(sourceSql);
        String emittedSql = null;

        try {
            SqlParser.create(parseCandidateSql, parserConfig).parseQuery();
            result.put("calcite_parse_succeeded", "true");
            result.put("route_stage_reached", "parse");

            List<ParsedTable> ddlTables = parseSimpleCreateTables(ddlSql);
            result.put("schema_ddl_ingestion_succeeded", "true");
            result.put("route_stage_reached", "schema_ingestion");

            FrameworkConfig config = buildFrameworkConfig(ddlTables, parserConfig);
            try (Planner planner = Frameworks.getPlanner(config)) {
                SqlNode plannerParsed = planner.parse(parseCandidateSql);
                SqlNode validatedQuery = planner.validate(plannerParsed);
                result.put("validation_succeeded", "true");
                result.put("route_stage_reached", "validate");

                RelRoot relRoot = planner.rel(validatedQuery);
                result.put("sql_to_rel_succeeded", "true");
                result.put("route_stage_reached", "sql_to_rel");

                RelNode hepRel = applyBoundedHepProgram(relRoot.rel);
                result.put("hep_planner_succeeded", "true");
                result.put("route_stage_reached", "hep_planner");

                RelToSqlConverter converter = new RelToSqlConverter(dialect);
                SqlNode relToSqlNode = converter.visitRoot(hepRel).asStatement();
                emittedSql = relToSqlNode.toSqlString(dialect).getSql();
                emittedSql = restoreAvgPrecision(emittedSql);
                result.put("rel_to_sql_succeeded", "true");
                result.put("route_stage_reached", "rel_to_sql");
            }
        } catch (Exception e) {
            result.put("blocker_reason", sanitizeForKv(firstUsefulMessage(e)));
            if (!"true".equals(result.get("calcite_parse_succeeded"))) {
                result.put("failure_category", "parser_failed");
                result.put("dialect_rendering_status", "parser_failed");
            } else {
                result.put("failure_category", "hep_rewrite_failed");
                result.put("dialect_rendering_status", "hep_rewrite_failed");
            }
        }

        if (emittedSql != null && !emittedSql.isBlank()) {
            Files.createDirectories(outputSqlPath.getParent());
            Files.writeString(outputSqlPath, emittedSql + System.lineSeparator(), StandardCharsets.UTF_8);
            result.put("candidate_sql_emitted", "true");
            result.put("dialect_rendering_status", "target_dialect_rendered");
            result.put("failure_category", "");
            result.put("blocker_reason", "");
            result.put(
                    "rewrite_changed",
                    Boolean.toString(!normalizeSql(sourceSql).equals(normalizeSql(emittedSql))));
        } else if (result.get("failure_category").isEmpty()) {
            result.put("failure_category", "generated_sql_missing");
            result.put("blocker_reason", "method_finished_without_nonempty_target_engine_sql");
            result.put("dialect_rendering_status", "rendered_sql_missing");
        }

        for (Map.Entry<String, String> entry : result.entrySet()) {
            System.out.println(entry.getKey() + "=" + sanitizeForKv(entry.getValue()));
        }
    }

    private static SqlDialect selectDialect(String engine) {
        switch (engine) {
            case "pg":
                return PostgresqlSqlDialect.DEFAULT;
            case "mysql":
                return MysqlSqlDialect.DEFAULT;
            case "spark":
                return SparkSqlDialect.DEFAULT;
            default:
                throw new IllegalArgumentException("unsupported target engine: " + engine);
        }
    }

    private static Lex selectParserLex(String engine) {
        switch (engine) {
            case "pg":
                return Lex.JAVA;
            case "mysql":
            case "spark":
                return Lex.MYSQL;
            default:
                throw new IllegalArgumentException("unsupported parser engine: " + engine);
        }
    }

    private static FrameworkConfig buildFrameworkConfig(List<ParsedTable> tables, SqlParser.Config parserConfig) {
        org.apache.calcite.schema.SchemaPlus rootSchema = Frameworks.createRootSchema(true);
        for (ParsedTable table : tables) {
            rootSchema.add(table.tableName, new StaticTable(table.columns));
        }
        return Frameworks.newConfigBuilder()
                .defaultSchema(rootSchema)
                .parserConfig(parserConfig)
                .build();
    }

    private static RelNode applyBoundedHepProgram(RelNode rel) {
        HepProgram hepProgram =
                new HepProgramBuilder().addRuleInstance(CoreRules.AGGREGATE_REDUCE_FUNCTIONS).build();
        HepPlanner planner = new HepPlanner(hepProgram);
        planner.setRoot(rel);
        return planner.findBestExp();
    }

    private static List<ParsedTable> parseSimpleCreateTables(String ddlSql) {
        String cleaned = stripSqlComments(ddlSql).trim();
        List<ParsedTable> tables = new ArrayList<>();
        int cursor = 0;
        String lowered = cleaned.toLowerCase(Locale.ROOT);
        while (true) {
            int createIndex = lowered.indexOf("create table", cursor);
            if (createIndex < 0) {
                break;
            }
            int nameStart = createIndex + "create table".length();
            while (nameStart < cleaned.length() && Character.isWhitespace(cleaned.charAt(nameStart))) {
                nameStart++;
            }
            if (cleaned.regionMatches(true, nameStart, "if not exists", 0, "if not exists".length())) {
                nameStart += "if not exists".length();
                while (nameStart < cleaned.length() && Character.isWhitespace(cleaned.charAt(nameStart))) {
                    nameStart++;
                }
            }

            String tableName;
            int nameEnd;
            char first = cleaned.charAt(nameStart);
            if (first == '`' || first == '"') {
                int close = cleaned.indexOf(first, nameStart + 1);
                if (close < 0) {
                    throw new IllegalArgumentException("could not parse table name from DDL");
                }
                tableName = cleaned.substring(nameStart + 1, close);
                nameEnd = close + 1;
            } else {
                nameEnd = nameStart;
                while (nameEnd < cleaned.length()) {
                    char c = cleaned.charAt(nameEnd);
                    if (Character.isLetterOrDigit(c) || c == '_') {
                        nameEnd++;
                    } else {
                        break;
                    }
                }
                if (nameEnd == nameStart) {
                    throw new IllegalArgumentException("could not parse table name from DDL");
                }
                tableName = cleaned.substring(nameStart, nameEnd);
            }

            int openParen = cleaned.indexOf('(', nameEnd);
            if (openParen < 0) {
                throw new IllegalArgumentException("could not find column list for table " + tableName);
            }
            int closeParen = findMatchingParen(cleaned, openParen);
            String columnSection = cleaned.substring(openParen + 1, closeParen);
            tables.add(new ParsedTable(tableName, parseColumns(columnSection)));
            cursor = closeParen + 1;
        }
        if (tables.isEmpty()) {
            throw new IllegalArgumentException("no CREATE TABLE statements parsed from DDL");
        }
        return tables;
    }

    private static int findMatchingParen(String text, int openIndex) {
        int depth = 0;
        for (int i = openIndex; i < text.length(); i++) {
            char c = text.charAt(i);
            if (c == '(') {
                depth++;
            } else if (c == ')') {
                depth--;
                if (depth == 0) {
                    return i;
                }
            }
        }
        throw new IllegalArgumentException("unbalanced parentheses in DDL");
    }

    private static List<ParsedColumn> parseColumns(String columnSection) {
        List<ParsedColumn> columns = new ArrayList<>();
        for (String rawPart : splitTopLevelComma(columnSection)) {
            String part = rawPart.trim();
            if (part.isEmpty()) {
                continue;
            }
            String lowered = part.toLowerCase(Locale.ROOT);
            if (lowered.startsWith("primary key")
                    || lowered.startsWith("unique")
                    || lowered.startsWith("constraint")
                    || lowered.startsWith("key ")
                    || lowered.startsWith("index ")
                    || lowered.startsWith("foreign key")) {
                continue;
            }
            Matcher matcher = COLUMN_PATTERN.matcher(part);
            if (!matcher.matches()) {
                continue;
            }
            String name = matcher.group(2);
            String typeName = matcher.group(4).toUpperCase(Locale.ROOT);
            String precisionPart = matcher.group(5);
            SqlTypeName sqlTypeName = mapType(typeName, precisionPart);
            Integer precision = parsePrecision(sqlTypeName, precisionPart);
            columns.add(new ParsedColumn(name, sqlTypeName, precision));
        }
        if (columns.isEmpty()) {
            throw new IllegalArgumentException("no supported columns parsed from DDL");
        }
        return columns;
    }

    private static List<String> splitTopLevelComma(String text) {
        List<String> parts = new ArrayList<>();
        int depth = 0;
        int start = 0;
        for (int i = 0; i < text.length(); i++) {
            char c = text.charAt(i);
            if (c == '(') {
                depth++;
            } else if (c == ')') {
                depth--;
            } else if (c == ',' && depth == 0) {
                parts.add(text.substring(start, i));
                start = i + 1;
            }
        }
        parts.add(text.substring(start));
        return parts;
    }

    private static SqlTypeName mapType(String typeName, String precisionPart) {
        switch (typeName) {
            case "INT":
            case "INTEGER":
            case "SERIAL":
                return SqlTypeName.INTEGER;
            case "BIGINT":
                return SqlTypeName.BIGINT;
            case "SMALLINT":
                return SqlTypeName.SMALLINT;
            case "DOUBLE":
            case "DOUBLE PRECISION":
            case "FLOAT":
                return SqlTypeName.DOUBLE;
            case "REAL":
                return SqlTypeName.REAL;
            case "DECIMAL":
            case "NUMERIC":
                return SqlTypeName.DECIMAL;
            case "BOOLEAN":
            case "BOOL":
                return SqlTypeName.BOOLEAN;
            case "DATE":
                return SqlTypeName.DATE;
            case "TIMESTAMP":
            case "DATETIME":
                return SqlTypeName.TIMESTAMP;
            case "CHAR":
                return SqlTypeName.CHAR;
            case "VARCHAR":
            case "STRING":
            case "TEXT":
                return SqlTypeName.VARCHAR;
            default:
                if (precisionPart != null && !precisionPart.isBlank()) {
                    return SqlTypeName.VARCHAR;
                }
                return SqlTypeName.VARCHAR;
        }
    }

    private static Integer parsePrecision(SqlTypeName typeName, String precisionPart) {
        if (precisionPart == null || precisionPart.isBlank()) {
            return null;
        }
        if (!(typeName == SqlTypeName.CHAR
                || typeName == SqlTypeName.VARCHAR
                || typeName == SqlTypeName.DECIMAL)) {
            return null;
        }
        String[] pieces = precisionPart.split(",");
        try {
            return Integer.parseInt(pieces[0].trim());
        } catch (NumberFormatException e) {
            return null;
        }
    }

    private static String stripSqlComments(String sql) {
        return sql.replaceAll("(?m)--.*$", " ").replaceAll("(?s)/\\*.*?\\*/", " ");
    }

    private static String stripTrailingSemicolon(String sql) {
        String trimmed = sql.trim();
        if (trimmed.endsWith(";")) {
            trimmed = trimmed.substring(0, trimmed.length() - 1).trim();
        }
        return trimmed;
    }

    private static String restoreAvgPrecision(String sql) {
        Matcher matcher = REDUCED_AVG_PATTERN.matcher(sql);
        return matcher.replaceAll("AVG($1)");
    }

    private static String normalizeSql(String sql) {
        String trimmed = sql.trim();
        if (trimmed.endsWith(";")) {
            trimmed = trimmed.substring(0, trimmed.length() - 1);
        }
        return trimmed.replaceAll("\\s+", " ").trim();
    }

    private static String sanitizeForKv(String value) {
        return value == null ? "" : value.replace("\n", " ").replace("\r", " ").trim();
    }

    private static String firstUsefulMessage(Throwable throwable) {
        Throwable cursor = throwable;
        while (cursor != null) {
            if (cursor.getMessage() != null && !cursor.getMessage().isBlank()) {
                return cursor.getMessage();
            }
            cursor = cursor.getCause();
        }
        return throwable.getClass().getName();
    }

    private static Map<String, String> parseArgs(String[] args) {
        LinkedHashMap<String, String> values = new LinkedHashMap<>();
        for (int i = 0; i < args.length; i += 2) {
            if (i + 1 >= args.length) {
                throw new IllegalArgumentException("expected value after " + args[i]);
            }
            values.put(args[i], args[i + 1]);
        }
        return values;
    }

    private static String requireArg(Map<String, String> values, String key) {
        String value = values.get(key);
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException("missing required arg " + key);
        }
        return value;
    }

    private static final class ParsedTable {
        final String tableName;
        final List<ParsedColumn> columns;

        ParsedTable(String tableName, List<ParsedColumn> columns) {
            this.tableName = tableName;
            this.columns = Collections.unmodifiableList(columns);
        }
    }

    private static final class ParsedColumn {
        final String name;
        final SqlTypeName typeName;
        final Integer precision;

        ParsedColumn(String name, SqlTypeName typeName, Integer precision) {
            this.name = name;
            this.typeName = typeName;
            this.precision = precision;
        }
    }

    private static final class StaticTable extends AbstractTable {
        private final List<ParsedColumn> columns;

        StaticTable(List<ParsedColumn> columns) {
            this.columns = columns;
        }

        @Override
        public RelDataType getRowType(RelDataTypeFactory typeFactory) {
            RelDataTypeFactory.Builder builder = typeFactory.builder();
            for (ParsedColumn column : columns) {
                RelDataType type =
                        column.precision == null
                                ? typeFactory.createSqlType(column.typeName)
                                : typeFactory.createSqlType(column.typeName, column.precision);
                builder.add(column.name, type);
            }
            return builder.build();
        }
    }
}
