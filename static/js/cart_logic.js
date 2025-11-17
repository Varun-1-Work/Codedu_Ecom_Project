// --- FILE: cart_logic.js ---

const CART_STORAGE_KEY = 'myShopCartItems';

// --- Utility Functions for Local Storage ---

function getCart() {
    try {
        const cartJson = localStorage.getItem(CART_STORAGE_KEY);
        return cartJson ? JSON.parse(cartJson) : [];
    } catch (error) {
        console.error("Error reading cart from localStorage:", error);
        return [];
    }
}

function saveCart(cart) {
    try {
        localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(cart));
    } catch (error) {
        console.error("Error saving cart to localStorage:", error);
    }
}

// --- Core Logic: Add, Remove, and Update Display ---

function updateCartCountDisplay() {
    const cart = getCart();
    const totalItems = cart.reduce((total, item) => total + item.quantity, 0);
    const countElement = document.getElementById('cart-count');
    if (countElement) {
        countElement.textContent = totalItems;
    }
}

function addToCart(product) {
    const cart = getCart();
    const existingItemIndex = cart.findIndex(item => item.id === product.id);

    if (existingItemIndex > -1) {
        cart[existingItemIndex].quantity += 1;
    } else {
        product.price = parseFloat(product.price);
        cart.push({ ...product, quantity: 1 });
    }

    saveCart(cart);
    updateCartCountDisplay();
    renderCart(); 
    showNotification(`${product.name} added to cart!`);
}

function renderCart() {
    const cart = getCart();
    const listContainer = document.getElementById('cart-items-list');
    const totalElement = document.getElementById('cart-total');
    const emptyMessage = document.getElementById('empty-cart-message');

    if (!listContainer) return; 

    // Temporarily remove empty message to reset
    if (emptyMessage) emptyMessage.style.display = 'none';
    listContainer.innerHTML = ''; // Clear previous contents

    if (cart.length === 0) {
        // Add empty message back if cart is empty
        if (emptyMessage) {
            listContainer.appendChild(emptyMessage);
            emptyMessage.style.display = 'block';
        }
        totalElement.textContent = '$0.00';
        return;
    }

    let subtotal = 0;

    cart.forEach(item => {
        const itemTotal = item.price * item.quantity;
        subtotal += itemTotal;

        // Create the display element for each item
        const itemDiv = document.createElement('div');
        itemDiv.className = 'cart-item';
        // Note: The image 'src' is now correctly read from the product object
        itemDiv.innerHTML = `
            <img src="${item.image}" alt="${item.name}">
            <div class="cart-item-details">
                <h4>${item.name}</h4>
                <p>$${item.price.toFixed(2)}</p>
                <input type="number" min="1" value="${item.quantity}" data-id="${item.id}" class="quantity-input">
            </div>
            <div class="cart-item-actions">
                <div class="item-price">$${itemTotal.toFixed(2)}</div>
                <button data-id="${item.id}" class="remove-item">Remove</button>
            </div>
        `;
        listContainer.appendChild(itemDiv);
    });

    totalElement.textContent = `$${subtotal.toFixed(2)}`;
}

function removeItemFromCart(productId) {
    let cart = getCart();
    cart = cart.filter(item => item.id !== productId);
    saveCart(cart);
    updateCartCountDisplay();
    renderCart();
    showNotification('Item removed from cart.', 'error');
}

function updateItemQuantity(productId, newQuantity) {
    let cart = getCart();
    const item = cart.find(item => item.id === productId);
    const parsedQuantity = parseInt(newQuantity, 10);

    if (item && parsedQuantity > 0) {
        item.quantity = parsedQuantity;
        saveCart(cart);
        updateCartCountDisplay();
        renderCart();
    } else if (parsedQuantity <= 0) {
        // If quantity is 0 or less, remove the item
        removeItemFromCart(productId);
    }
}

// --- UI Helper: Notification Message ---

function showNotification(message, type = 'success') {
    const existingNotif = document.getElementById('app-notification');
    if (existingNotif) existingNotif.remove();

    const notif = document.createElement('div');
    notif.id = 'app-notification';
    notif.textContent = message;
    if (type === 'error') {
        notif.classList.add('error');
    }
    
    document.body.appendChild(notif);
    
    // Animate in
    setTimeout(() => {
        notif.classList.add('show');
    }, 10);
    
    // Animate out after 3 seconds
    setTimeout(() => {
        notif.classList.remove('show');
        // Remove from DOM after animation finishes
        setTimeout(() => notif.remove(), 300);
    }, 3000);
}

// --- Initialization and Event Delegation ---
// This runs when your page is fully loaded

document.addEventListener('DOMContentLoaded', () => {
    
    // --- Cart Sidebar Controls ---
    const cartBtn = document.getElementById('cart-btn');
    const closeBtn = document.getElementById('close-cart-btn');
    const backdrop = document.getElementById('cart-backdrop');
    const sidebar = document.getElementById('cart-sidebar');

    function openCart() {
        if (sidebar) sidebar.classList.add('open');
        if (backdrop) backdrop.classList.add('open');
        renderCart(); // Re-draw the cart every time it's opened
    }

    function closeCart() {
        if (sidebar) sidebar.classList.remove('open');
        if (backdrop) backdrop.classList.remove('open');
    }

    if (cartBtn) cartBtn.addEventListener('click', openCart);
    if (closeBtn) closeBtn.addEventListener('click', closeCart);
    if (backdrop) backdrop.addEventListener('click', closeCart);


    // --- Add to Cart Button Listener ---
    // This finds ALL "Add to Cart" buttons on the page
    document.querySelectorAll('.add-to-cart-btn').forEach(button => {
        button.addEventListener('click', (event) => {
            // Find the main product 'box'
            const card = event.target.closest('.product-card');
            
            if (card) {
                // Get the data we stored in the HTML
                const product = {
                    id: card.dataset.id,
                    name: card.dataset.name,
                    price: card.dataset.price,
                    image: card.dataset.image
                };
                addToCart(product);
            } else {
                console.error("Could not find product card for this button.");
            }
        });
    });

    // --- Actions inside the cart (Remove, Quantity change) ---
    // Using event delegation on the list container
    const cartList = document.getElementById('cart-items-list');

    if (cartList) {
        cartList.addEventListener('click', (event) => {
            if (event.target.classList.contains('remove-item')) {
                const productId = event.target.dataset.id;
                removeItemFromCart(productId);
            }
        });

        cartList.addEventListener('change', (event) => {
            if (event.target.classList.contains('quantity-input')) {
                const productId = event.target.dataset.id;
                const newQuantity = event.target.value;
                updateItemQuantity(productId, newQuantity);
            }
        });
    }

    // --- Checkout Button Placeholder ---
    const checkoutBtn = document.getElementById('checkout-btn');
    if(checkoutBtn) {
        checkoutBtn.addEventListener('click', () => {
            showNotification("Checkout is not implemented in this demo.", 'error');
        });
    }

    // --- Initial Load ---
    // Update the cart count in the header as soon as the page loads
    updateCartCountDisplay();
});