package org.hkust.utils;

import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.hkust.objects.Node;

/**
 * Helper class to build Flink streaming jobs from Node objects.
 *
 * TODO: Implement the following:
 * - Create StreamExecutionEnvironment with proper configuration
 * - Set up data source (file, socket, or Kafka)
 * - Parse input lines using TPCHDataParser
 * - Route tuples to appropriate process functions based on table name
 * - Connect RelationProcessFunctions in join order
 * - Connect AggregateProcessFunctions for final aggregation
 * - Set up output sink (console or file)
 * - Configure checkpointing and state backend
 * - Set parallelism
 */
public class FlinkJobBuilder {

    /**
     * Build a Flink streaming job from a Node object.
     *
     * @param node Query execution plan
     * @param env Flink execution environment
     * @param inputPath Path to input data file
     * @param outputPath Path to output file (or null for console)
     * @return Configured DataStream
     */
    public static DataStream<?> buildJob(Node node,
                                          StreamExecutionEnvironment env,
                                          String inputPath,
                                          String outputPath) {
        // TODO: Implement job building logic

        // Steps:
        // 1. Create data source from inputPath
        // 2. Parse lines into TPCHTuple objects
        // 3. Filter/route by table name
        // 4. For each RelationProcessFunction:
        //    - Create KeyedProcessFunction
        //    - Key by appropriate field
        //    - Connect to parent RelationProcessFunction
        // 5. For each AggregateProcessFunction:
        //    - Create KeyedProcessFunction
        //    - Key by group-by fields
        // 6. Add output sink
        // 7. Return final DataStream

        throw new UnsupportedOperationException("Job building not yet implemented");
    }
}
