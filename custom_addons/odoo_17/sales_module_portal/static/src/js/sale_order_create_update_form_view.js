<script>
        document.getElementById('rendered-text').innerText = "Hello, this text is rendered by JavaScript!";

//    document.addEventListener('DOMContentLoaded', () => {
//        const addProductBtn = document.getElementById('add-product');
//        const productList = document.getElementById('product-list');
//        const orderLinesInput = document.getElementById('order_lines');
//
//        let orderLines = [];
//
//        addProductBtn.addEventListener('click', () => {
//            const productSelect = document.getElementById('product');
//            const quantityInput = document.getElementById('quantity');
//
//            const productId = productSelect.value;
//            const productName = productSelect.options[productSelect.selectedIndex]?.text;
//            const quantity = parseInt(quantityInput.value, 10);
//
//            if (!productId || quantity < 1) {
//                alert('Please select a product and enter a valid quantity.');
//                return;
//            }
//
//            // Add product to the order lines
//            const orderLine = {
//                product_id: productId,
//                product_name: productName,
//                quantity: quantity,
//            };
//            orderLines.push(orderLine);
//
//            // Update the UI
//            const listItem = document.createElement('li');
//            listItem.setAttribute('data-product-id', productId);
//            listItem.style.marginBottom = '10px';
//
//            listItem.innerHTML = `
//                ${productName} (x${quantity})
//                <button type="button" class="btn btn-danger btn-sm remove-product" style="margin-left: 10px;">Remove</button>
//            `;
//
//            productList.appendChild(listItem);
//
//            // Update the hidden input value
//            updateOrderLinesInput();
//
//            // Add event listener to the remove button
//            listItem.querySelector('.remove-product').addEventListener('click', () => {
//                productList.removeChild(listItem);
//                orderLines = orderLines.filter(line => line.product_id !== productId);
//                updateOrderLinesInput();
//            });
//
//            // Reset product and quantity input
//            productSelect.value = '';
//            quantityInput.value = 1;
//        });
//
//        function updateOrderLinesInput() {
//            orderLinesInput.value = JSON.stringify(orderLines);
//        }
//    });
</script>
