package org.hkust;

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.hkust.objects.Node;
import org.hkust.parser.SQLParser;
import org.hkust.parser.JSONParser;
import org.hkust.utils.FlinkJobBuilder;
import picocli.CommandLine;
import picocli.CommandLine.Command;
import picocli.CommandLine.Option;

import java.util.concurrent.Callable;

/**
 * Main entry point for Cquirrel Reproduction project.
 *
 * This program:
 * 1. Parses SQL query or JSON configuration
 * 2. Builds Flink streaming job
 * 3. Executes the job on input TPC-H data
 * 4. Outputs results to console or file
 *
 * Usage:
 *   # Using SQL
 *   java -jar cquirrel-reproduction.jar --sql "SELECT ..." --input data.csv --output result.txt
 *
 *   # Using JSON
 *   java -jar cquirrel-reproduction.jar --json query.json --input data.csv --output result.txt
 *
 * TODO: Implement the following:
 * - Command line argument parsing
 * - SQL/JSON input handling
 * - Flink environment setup
 * - Job execution and result collection
 * - Error handling and logging
 */
@Command(name = "cquirrel", mixinStandardHelpOptions = true, version = "1.0",
         description = "Cquirrel: SQL to Flink Streaming Code Generator for TPC-H")
public class CquirrelMain implements Callable<Integer> {

    @Option(names = {"-s", "--sql"}, description = "SQL query string")
    private String sqlQuery;

    @Option(names = {"-j", "--json"}, description = "Path to JSON configuration file")
    private String jsonFile;

    @Option(names = {"-i", "--input"}, required = true,
            description = "Path to input TPC-H data file (e.g., input_data_all.csv)")
    private String inputPath;

    @Option(names = {"-o", "--output"},
            description = "Path to output file (default: console)")
    private String outputPath;

    @Option(names = {"-p", "--parallelism"},
            description = "Flink parallelism (default: 1)")
    private int parallelism = 1;

    public static void main(String[] args) {
        int exitCode = new CommandLine(new CquirrelMain()).execute(args);
        System.exit(exitCode);
    }

    @Override
    public Integer call() throws Exception {
        // TODO: Implement main execution logic

        System.out.println("=== Cquirrel Reproduction ===");

        // Validate input
        if (sqlQuery == null && jsonFile == null) {
            System.err.println("Error: Either --sql or --json must be provided");
            return 1;
        }

        if (sqlQuery != null && jsonFile != null) {
            System.err.println("Error: Cannot provide both --sql and --json");
            return 1;
        }

        try {
            // Step 1: Parse query into Node object
            Node node = parseQuery();
            System.out.println("Query parsed successfully");

            // Step 2: Set up Flink environment
            StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
            env.setParallelism(parallelism);
            System.out.println("Flink environment initialized (parallelism=" + parallelism + ")");

            // Step 3: Build Flink job
            System.out.println("Building Flink job...");
            FlinkJobBuilder.buildJob(node, env, inputPath, outputPath);

            // Step 4: Execute job
            System.out.println("Executing Flink job...");
            System.out.println("Input: " + inputPath);
            if (outputPath != null) {
                System.out.println("Output: " + outputPath);
            } else {
                System.out.println("Output: console");
            }

            env.execute("Cquirrel TPC-H Query");

            System.out.println("\n=== Execution completed successfully ===");
            return 0;

        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
            return 1;
        }
    }

    /**
     * Parse SQL or JSON input into a Node object.
     */
    private Node parseQuery() throws Exception {
        if (sqlQuery != null) {
            System.out.println("Parsing SQL query...");
            SQLParser parser = new SQLParser();
            return parser.parseSQL(sqlQuery);
        } else {
            System.out.println("Parsing JSON file: " + jsonFile);
            JSONParser parser = new JSONParser();
            return parser.parseJSON(jsonFile);
        }
    }
}
