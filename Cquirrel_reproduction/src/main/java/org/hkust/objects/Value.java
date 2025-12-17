package org.hkust.objects;

/**
 * Interface representing a value in expressions.
 * A value can be:
 * - ConstantValue: A literal constant (e.g., "BUILDING", 10, 3.14)
 * - AttributeValue: A column reference (e.g., c_mktsegment, l_quantity)
 * - Expression: A binary operation combining two values (e.g., l_extendedprice * (1 - l_discount))
 *
 * TODO: Implement the following concrete classes:
 * - ConstantValue (with data type and value)
 * - AttributeValue (with attribute name and relation)
 * - Expression (with left/right values and operator)
 *
 * Each implementation should have:
 * - Method to evaluate the value from a tuple
 * - Method to get the data type
 * - Method to generate code for this value
 */
public interface Value {
    /**
     * Get the type of this value (constant, attribute, or expression)
     */
    String getType();

    /**
     * Get the data type of this value (INTEGER, DOUBLE, VARCHAR, DATE)
     */
    String getDataType();

    // TODO: Add methods for evaluation and code generation
}
