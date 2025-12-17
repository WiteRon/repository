package org.hkust.objects;

/**
 * Represents a WHERE clause condition in SQL.
 *
 * TODO: Implement the following:
 * - Left operand (Value)
 * - Right operand (Value)
 * - Comparison operator (=, <, >, <=, >=, !=, LIKE, etc.)
 * - Logical operator to combine with other conditions (AND, OR)
 * - Method to evaluate the condition on a tuple
 */
public class SelectCondition {
    private Value leftValue;
    private Value rightValue;
    private String operator;

    // TODO: Add full implementation

    public Value getLeftValue() {
        return leftValue;
    }

    public Value getRightValue() {
        return rightValue;
    }

    public String getOperator() {
        return operator;
    }
}
