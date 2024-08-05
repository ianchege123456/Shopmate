import React, { useContext, useState } from 'react';
import { ProductContext } from '../../context/ProductContext';
import ProductDetail from './ProductDetail';
import Pagination from '../Pagination';

const ProductList = () => {
    const { products, loading } = useContext(ProductContext);
    const [currentPage, setCurrentPage] = useState(1);
    const [productsPerPage] = useState(10);

    const indexOfLastProduct = currentPage * productsPerPage;
    const indexOfFirstProduct = indexOfLastProduct - productsPerPage;
    const currentProducts = products.slice(indexOfFirstProduct, indexOfLastProduct);

    const paginate = (pageNumber) => setCurrentPage(pageNumber);

    if (loading) {
        return <p>Loading...</p>;
    }

    return (
        <div>
            <div className="product-list">
                {currentProducts.map(product => (                    
                    <ProductDetail key={product.id} product={product} />
                    
                ))}
            </div>
            <Pagination
                productsPerPage={productsPerPage}
                totalProducts={products.length}
                paginate={paginate}
            />
        </div>
    );
};

export default ProductList;
