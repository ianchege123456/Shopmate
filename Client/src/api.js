////////const API_URL = 'https://localhost:5555';

export const login = async (data) => {
  const response = await fetch(`/login`, {
    method: 'POST',
    headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
  });
      // console.log('Login response:', result);

  if (!response.ok) {
      throw new Error('Login failed');
  }

  const result = await response.json();
  
  // Log the entire result to see if the token is included
  
  // Save the access token to local storage
  localStorage.setItem('token', result.access_token);
  
  // Log the token after saving to local storage
  console.log('Saved token:', localStorage.getItem('token'));
  
  return result;
};

  export const register = async (data) => {
    const response = await fetch(`/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
  
    if (!response.ok) {
      throw new Error('Registration failed');
    }
  
    return response.json();
  };
  
  export const fetchProducts = async () => {
    const response = await fetch(`/products`);
    if (!response.ok) {
      throw new Error('Failed to fetch products');
    }
    return response.json();
  };
  
  export async function filterProducts({ category, minPrice, maxPrice, sortBy, page, perPage }) {
    const queryParams = new URLSearchParams({
        category,
        min_price: minPrice,
        max_price: maxPrice,
        sort_by: sortBy,
        page,
        per_page: perPage
    }).toString();

    const response = await fetch(`/products?${queryParams}`);
    if (!response.ok) {
        throw new Error('Failed to fetch products');
    }
    return response.json();
}

export async function fetchProduct(productId) {
    const response = await fetch(`/products/${productId}`);
    if (!response.ok) {
        throw new Error('Failed to fetch product details');
    }
    return response.json();
}

export const fetchCartItems = async () => {
  const token = localStorage.getItem('token');
  
  if (!token) {
      throw new Error('No token found, please log in again');
  }

  const response = await fetch(`/carts`, {
      headers: {
          'Authorization': `Bearer ${token}`,
      },
  });

  if (!response.ok) {
      throw new Error('Failed to fetch cart items');
  }

  return response.json();
};
export const addToCart = async (productId, quantity) => {
  const token = localStorage.getItem('token');

  if (!token) {
    throw new Error('No token found, please log in again');
  }

  const response = await fetch(`/cart`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({ product_id: productId, quantity }),
  });

  if (!response.ok) {
    throw new Error('Failed to add item to cart');
  }

  return response.json();
};


  export const fetchOrderHistory = async () => {
    const response = await fetch(`/orders`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
    });
    if (!response.ok) {
      throw new Error('Failed to fetch order history');
    }
    return response.json();
  };
  
  export const fetchUserProfile = async () => {
    const response = await fetch(`/profile`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
    });
    if (!response.ok) {
      throw new Error('Failed to fetch user profile');
    }
    return response.json();
  };
  
  export const updateUserProfile = async (data) => {
    const response = await fetch(`/profile`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
      body: JSON.stringify(data),
    });
  
    if (!response.ok) {
      throw new Error('Failed to update profile');
    }
  };
  
  export const submitSupportRequest = async (data) => {
    const response = await fetch(`/support`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
      },
      body: JSON.stringify(data),
    });
  
    if (!response.ok) {
      throw new Error('Failed to submit support request');
    }
  };
  
