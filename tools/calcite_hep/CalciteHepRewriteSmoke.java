import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
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
import org.apache.calcite.schema.Table;
import org.apache.calcite.schema.impl.AbstractTable;
import org.apache.calcite.sql.SqlNode;
import org.apache.calcite.sql.dialect.PostgresqlSqlDialect;
import org.apache.calcite.sql.parser.SqlParser;
import org.apache.calcite.sql.type.SqlTypeName;
import org.apache.calcite.tools.FrameworkConfig;
import org.apache.calcite.tools.Frameworks;
import org.apache.calcite.tools.Planner;

public final class CalciteHepRewriteSmoke {
    private static final Pattern CREATE_TABLE_PATTERN =
            Pattern.compile("(?is)create\\s+table\\s+([a-zA-Z_][\\w]*)\\s*\\((.*)\\)\\s*;?\\s*");
    private static final Pattern COLUMN_PATTERN =
            Pattern.compile(
                    "(?is)^([a-zA-Z_][\\w]*)\\s+([a-zA-Z]+)(?:\\s*\\(([^)]*)\\))?(?:\\s+(not\\s+null))?$");

    private CalciteHepRewriteSmoke() {}

    public static void main(String[] args) throws Exception {
        Map<String, String> parsed = parseArgs(args);
        String caseId = requireArg(parsed, "--case-id");
        Path sourceSqlPath = Path.of(requireArg(parsed, "--source-sql"));
        Path ddlPath = Path.of(requireArg(parsed, "--ddl"));
        Path outputSqlPath = Path.of(requireArg(parsed, "--output-sql"));
        RouteMode routeMode = RouteMode.fromArg(parsed.getOrDefault("--mode", "scaffold_parse_only"));

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

        if (routeMode == RouteMode.SCAFFOLD_PARSE_ONLY) {
            runScaffoldMode(caseId, sourceSql, ddlSql, outputSqlPath);
            return;
        }
        runRealRouteCanary(caseId, sourceSql, ddlSql, outputSqlPath);
    }

    private static void runScaffoldMode(String caseId, String sourceSql, String ddlSql, Path outputSqlPath)
            throws Exception {
        String parseCandidateSql = stripTrailingSemicolon(sourceSql);
        SqlParser parser = SqlParser.create(parseCandidateSql);
        SqlNode parsedQuery = parser.parseQuery();

        Files.createDirectories(outputSqlPath.getParent());
        Files.writeString(outputSqlPath, sourceSql, StandardCharsets.UTF_8);

        System.out.println("case_id=" + caseId);
        System.out.println("route_mode=scaffold_parse_only");
        System.out.println("scaffold_status=adapter_parse_scaffold_only");
        System.out.println("source_sql_accepted=true");
        System.out.println("ddl_accepted=true");
        System.out.println("calcite_parse_succeeded=true");
        System.out.println("candidate_sql_emitted=true");
        System.out.println("emission_mode=original_passthrough");
        System.out.println("parsed_sql_kind=" + parsedQuery.getKind());
        System.out.println("source_sql_character_count=" + sourceSql.length());
        System.out.println("ddl_character_count=" + ddlSql.length());
        System.out.println("output_sql_path=" + outputSqlPath);
    }

    private static void runRealRouteCanary(String caseId, String sourceSql, String ddlSql, Path outputSqlPath)
            throws Exception {
        LinkedHashMap<String, String> result = new LinkedHashMap<>();
        result.put("case_id", caseId);
        result.put("route_mode", "real_route_canary");
        result.put("source_sql_accepted", "true");
        result.put("ddl_accepted", "true");
        result.put("schema_ddl_ingestion_succeeded", "false");
        result.put("calcite_parse_succeeded", "false");
        result.put("validation_succeeded", "false");
        result.put("sql_to_rel_succeeded", "false");
        result.put("hep_planner_succeeded", "false");
        result.put("rel_to_sql_succeeded", "false");
        result.put("candidate_sql_emitted", "false");
        result.put("emission_mode", "failed");
        result.put("route_stage_reached", "read_inputs");
        result.put("blocker_stage", "");
        result.put("blocker_message", "");
        result.put("emitted_sql_is_calcite_generated", "false");
        result.put("source_sql_character_count", Integer.toString(sourceSql.length()));
        result.put("ddl_character_count", Integer.toString(ddlSql.length()));

        boolean finalSemicolonNormalized = sourceSql.trim().endsWith(";");
        result.put("final_semicolon_normalized_for_parse", Boolean.toString(finalSemicolonNormalized));

        String parseCandidateSql = stripTrailingSemicolon(sourceSql);
        SqlNode parsedQuery = null;
        SqlNode validatedQuery = null;
        RelRoot relRoot = null;
        RelNode hepRel = null;
        ParsedTable ddlTable = null;
        String emittedSql = null;

        try {
            SqlParser.Config parserConfig = SqlParser.config().withLex(Lex.MYSQL);
            parsedQuery = SqlParser.create(parseCandidateSql, parserConfig).parseQuery();
            result.put("calcite_parse_succeeded", "true");
            result.put("parsed_sql_kind", parsedQuery.getKind().name());
            result.put("route_stage_reached", "parse");

            ddlTable = parseSimpleCreateTable(ddlSql);
            result.put("schema_ddl_ingestion_succeeded", "true");
            result.put("schema_table_name", ddlTable.tableName);
            result.put("schema_column_count", Integer.toString(ddlTable.columns.size()));

            FrameworkConfig config = buildFrameworkConfig(ddlTable, parserConfig);
            try (Planner planner = Frameworks.getPlanner(config)) {
                SqlNode plannerParsed = planner.parse(parseCandidateSql);
                validatedQuery = planner.validate(plannerParsed);
                result.put("validation_succeeded", "true");
                result.put("route_stage_reached", "validate");

                relRoot = planner.rel(validatedQuery);
                result.put("sql_to_rel_succeeded", "true");
                result.put("route_stage_reached", "sql_to_rel");

                hepRel = applyBoundedHepProgram(relRoot.rel);
                result.put("hep_planner_succeeded", "true");
                result.put("route_stage_reached", "hep_planner");

                RelToSqlConverter converter = new RelToSqlConverter(PostgresqlSqlDialect.DEFAULT);
                SqlNode relToSqlNode = converter.visitRoot(hepRel).asStatement();
                emittedSql = relToSqlNode.toSqlString(PostgresqlSqlDialect.DEFAULT).getSql();
                result.put("rel_to_sql_succeeded", "true");
                result.put("route_stage_reached", "rel_to_sql");
                result.put("emission_mode", "calcite_rel_to_sql");
                result.put("emitted_sql_is_calcite_generated", "true");
            }
        } catch (Exception e) {
            result.put("blocker_message", sanitizeForKv(firstUsefulMessage(e)));
            if ("true".equals(result.get("calcite_parse_succeeded")) && emittedSql == null && parsedQuery != null) {
                emittedSql = parsedQuery.toSqlString(PostgresqlSqlDialect.DEFAULT).getSql();
                result.put("emission_mode", "calcite_parse_only");
                result.put("emitted_sql_is_calcite_generated", "true");
            }
            if ("true".equals(result.get("rel_to_sql_succeeded"))) {
                result.put("blocker_stage", "");
            } else if ("true".equals(result.get("hep_planner_succeeded"))) {
                result.put("blocker_stage", "rel_to_sql");
            } else if ("true".equals(result.get("sql_to_rel_succeeded"))) {
                result.put("blocker_stage", "hep_planner");
            } else if ("true".equals(result.get("validation_succeeded"))) {
                result.put("blocker_stage", "sql_to_rel");
            } else if ("true".equals(result.get("schema_ddl_ingestion_succeeded"))) {
                result.put("blocker_stage", "validate");
            } else if ("true".equals(result.get("calcite_parse_succeeded"))) {
                result.put("blocker_stage", "schema_ingestion");
            } else {
                result.put("blocker_stage", "parse");
            }
        }

        if (emittedSql != null && !emittedSql.isBlank()) {
            Files.createDirectories(outputSqlPath.getParent());
            Files.writeString(outputSqlPath, emittedSql + System.lineSeparator(), StandardCharsets.UTF_8);
            result.put("candidate_sql_emitted", "true");
            result.put("output_sql_path", outputSqlPath.toString());
            result.put("emitted_sql_character_count", Integer.toString(emittedSql.length()));
            result.put("route_stage_reached", "emit");
        } else {
            result.put("output_sql_path", outputSqlPath.toString());
            result.put("emitted_sql_character_count", "0");
        }

        if ("true".equals(result.get("candidate_sql_emitted"))
                && "calcite_rel_to_sql".equals(result.get("emission_mode"))
                && result.get("blocker_stage").isEmpty()) {
            result.put("blocker_message", "");
        }

        for (Map.Entry<String, String> entry : result.entrySet()) {
            System.out.println(entry.getKey() + "=" + sanitizeForKv(entry.getValue()));
        }
    }

    private static FrameworkConfig buildFrameworkConfig(ParsedTable table, SqlParser.Config parserConfig) {
        org.apache.calcite.schema.SchemaPlus rootSchema = Frameworks.createRootSchema(true);
        rootSchema.add(table.tableName, new StaticTable(table.columns));
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

    private static ParsedTable parseSimpleCreateTable(String ddlSql) {
        String cleaned = stripSqlComments(ddlSql).trim();
        Matcher tableMatcher = CREATE_TABLE_PATTERN.matcher(cleaned);
        if (!tableMatcher.matches()) {
            throw new IllegalArgumentException("unsupported DDL format for canary parser");
        }
        String tableName = tableMatcher.group(1).trim();
        String columnsBody = tableMatcher.group(2).trim();
        List<String> columnChunks = splitTopLevelCommaList(columnsBody);
        List<ColumnDef> columns = new ArrayList<>();
        for (String rawColumn : columnChunks) {
            String normalized = rawColumn.trim();
            if (normalized.isEmpty()) {
                continue;
            }
            Matcher columnMatcher = COLUMN_PATTERN.matcher(normalized);
            if (!columnMatcher.matches()) {
                throw new IllegalArgumentException("unsupported column definition: " + normalized);
            }
            String columnName = columnMatcher.group(1).trim();
            String typeName = columnMatcher.group(2).trim().toLowerCase(Locale.ROOT);
            String typeArgs = columnMatcher.group(3);
            boolean notNull = columnMatcher.group(4) != null;
            columns.add(new ColumnDef(columnName, sqlTypeName(typeName), parseTypeArgs(typeArgs), !notNull));
        }
        if (columns.isEmpty()) {
            throw new IllegalArgumentException("no columns parsed from DDL");
        }
        return new ParsedTable(tableName, columns);
    }

    private static String stripSqlComments(String sql) {
        StringBuilder builder = new StringBuilder();
        for (String line : sql.split("\\R")) {
            String trimmed = line.trim();
            if (!trimmed.startsWith("--")) {
                builder.append(line).append('\n');
            }
        }
        return builder.toString();
    }

    private static List<String> splitTopLevelCommaList(String value) {
        List<String> chunks = new ArrayList<>();
        StringBuilder current = new StringBuilder();
        int depth = 0;
        for (int i = 0; i < value.length(); i++) {
            char c = value.charAt(i);
            if (c == '(') {
                depth++;
            } else if (c == ')') {
                depth--;
            }
            if (c == ',' && depth == 0) {
                chunks.add(current.toString());
                current.setLength(0);
                continue;
            }
            current.append(c);
        }
        if (current.length() > 0) {
            chunks.add(current.toString());
        }
        return chunks;
    }

    private static SqlTypeName sqlTypeName(String typeName) {
        switch (typeName) {
            case "char":
                return SqlTypeName.CHAR;
            case "varchar":
                return SqlTypeName.VARCHAR;
            case "numeric":
            case "decimal":
                return SqlTypeName.DECIMAL;
            case "date":
                return SqlTypeName.DATE;
            case "int":
            case "integer":
                return SqlTypeName.INTEGER;
            case "bigint":
                return SqlTypeName.BIGINT;
            default:
                throw new IllegalArgumentException("unsupported SQL type in canary DDL parser: " + typeName);
        }
    }

    private static List<Integer> parseTypeArgs(String typeArgs) {
        if (typeArgs == null || typeArgs.isBlank()) {
            return Collections.emptyList();
        }
        List<Integer> values = new ArrayList<>();
        for (String piece : typeArgs.split(",")) {
            values.add(Integer.parseInt(piece.trim()));
        }
        return values;
    }

    private static String stripTrailingSemicolon(String sql) {
        String trimmed = sql.trim();
        if (trimmed.endsWith(";")) {
            return trimmed.substring(0, trimmed.length() - 1);
        }
        return trimmed;
    }

    private static String sanitizeForKv(String value) {
        return value.replace("\r", " ").replace("\n", " ").trim();
    }

    private static String firstUsefulMessage(Throwable throwable) {
        Throwable current = throwable;
        while (current != null) {
            if (current.getMessage() != null && !current.getMessage().isBlank()) {
                return current.getClass().getSimpleName() + ": " + current.getMessage();
            }
            current = current.getCause();
        }
        return throwable.getClass().getSimpleName();
    }

    private static Map<String, String> parseArgs(String[] args) {
        Map<String, String> parsed = new HashMap<>();
        for (int i = 0; i < args.length; i += 2) {
            if (i + 1 >= args.length) {
                throw new IllegalArgumentException("missing value for argument: " + args[i]);
            }
            parsed.put(args[i], args[i + 1]);
        }
        return parsed;
    }

    private static String requireArg(Map<String, String> parsed, String key) {
        String value = parsed.get(key);
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException("required argument missing: " + key);
        }
        return value;
    }

    private enum RouteMode {
        SCAFFOLD_PARSE_ONLY,
        REAL_ROUTE_CANARY;

        static RouteMode fromArg(String value) {
            String normalized = value.trim().toLowerCase(Locale.ROOT);
            switch (normalized) {
                case "scaffold_parse_only":
                    return SCAFFOLD_PARSE_ONLY;
                case "real_route_canary":
                    return REAL_ROUTE_CANARY;
                default:
                    throw new IllegalArgumentException("unsupported wrapper mode: " + value);
            }
        }
    }

    private static final class ParsedTable {
        final String tableName;
        final List<ColumnDef> columns;

        ParsedTable(String tableName, List<ColumnDef> columns) {
            this.tableName = tableName;
            this.columns = List.copyOf(columns);
        }
    }

    private static final class ColumnDef {
        final String name;
        final SqlTypeName typeName;
        final List<Integer> typeArgs;
        final boolean nullable;

        ColumnDef(String name, SqlTypeName typeName, List<Integer> typeArgs, boolean nullable) {
            this.name = name;
            this.typeName = typeName;
            this.typeArgs = List.copyOf(typeArgs);
            this.nullable = nullable;
        }

        RelDataType toRelType(RelDataTypeFactory typeFactory) {
            RelDataType baseType;
            switch (typeName) {
                case CHAR:
                case VARCHAR:
                    int charPrecision = typeArgs.isEmpty() ? 1 : typeArgs.get(0);
                    baseType = typeFactory.createSqlType(typeName, charPrecision);
                    break;
                case DECIMAL:
                    if (typeArgs.size() == 2) {
                        baseType = typeFactory.createSqlType(typeName, typeArgs.get(0), typeArgs.get(1));
                    } else if (typeArgs.size() == 1) {
                        baseType = typeFactory.createSqlType(typeName, typeArgs.get(0));
                    } else {
                        baseType = typeFactory.createSqlType(typeName);
                    }
                    break;
                default:
                    baseType = typeFactory.createSqlType(typeName);
                    break;
            }
            return typeFactory.createTypeWithNullability(baseType, nullable);
        }
    }

    private static final class StaticTable extends AbstractTable {
        private final List<ColumnDef> columns;

        StaticTable(List<ColumnDef> columns) {
            this.columns = List.copyOf(columns);
        }

        @Override
        public RelDataType getRowType(RelDataTypeFactory typeFactory) {
            RelDataTypeFactory.Builder builder = new RelDataTypeFactory.Builder(typeFactory);
            for (ColumnDef column : columns) {
                builder.add(column.name, column.toRelType(typeFactory));
            }
            return builder.build();
        }
    }
}
