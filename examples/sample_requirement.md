# Requirement: Shopping Cart Checkout Optimization

## Background
Optimize the checkout flow - users can modify item quantity in cart and checkout directly.

## Functional Requirements
1. Users can modify item quantity (1-99) in cart
2. Subtotal updates in real-time on quantity change
3. Show warning and disable checkout when stock insufficient
4. Support batch item selection for checkout
5. Redirect to payment page after order placed

## Acceptance Criteria
- Quantity 0 auto-removes item
- Button disabled when quantity exceeds stock
- Amount precision: 2 decimal places
- Order API response time < 500ms
