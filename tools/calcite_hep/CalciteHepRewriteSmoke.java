import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.Map;

import org.apache.calcite.sql.SqlNode;
import org.apache.calcite.sql.parser.SqlParser;

public final class CalciteHepRewriteSmoke {
    private CalciteHepRewriteSmoke() {}

    public static void main(String[] args) throws Exception {
        Map<String, String> parsed = parseArgs(args);
        String caseId = requireArg(parsed, "--case-id");
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

        String parseCandidateSql = stripTrailingSemicolon(sourceSql);
        SqlParser parser = SqlParser.create(parseCandidateSql);
        SqlNode parsedQuery = parser.parseQuery();

        Files.createDirectories(outputSqlPath.getParent());
        Files.writeString(outputSqlPath, sourceSql, StandardCharsets.UTF_8);

        System.out.println("case_id=" + caseId);
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

    private static String stripTrailingSemicolon(String sql) {
        String trimmed = sql.trim();
        if (trimmed.endsWith(";")) {
            return trimmed.substring(0, trimmed.length() - 1);
        }
        return trimmed;
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
}
