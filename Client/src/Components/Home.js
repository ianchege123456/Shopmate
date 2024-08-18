import React, { useState, useEffect } from 'react'
import "./Home.css"
import { Link } from "react-router-dom";
import Product from "./Product";
import Marketing from "../Components/Marketing";
import Heading from "../Components/Heading";
import { data } from "../Library/stock";


function SectionBelowHeader() {
  const images = [
    { src: "Gas Cookers.jpeg", alt: "Electronics", link: "/category/electronics" },
    { src: "https://i.pinimg.com/originals/d8/34/89/d834891a49605bc17f503a7e17e804b8.jpg", alt: "Fashion", link: "/category/fashion" },
    { src: "https://i.pinimg.com/564x/10/b0/88/10b0884308bc91b4a3685bdd4e20d789.jpg", alt: "Home", link: "/category/home" },
    // Add more images as needed
  ];

  const [currentImageIndex, setCurrentImageIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentImageIndex((prevIndex) =>
        prevIndex === images.length - 1 ? 0 : prevIndex + 1
      );
    }, 3000); // Change image every 3 seconds

    return () => clearInterval(interval);
  }, [images.length]);
  return (
    <div className="homepage">
      <div className="section-below-header">
        {/* Categories Section */}
        <div className="categories">
          <h3>Categories</h3>
          <ul>
            <li><Link to="/category/electronics">Electronics</Link></li>
            <li><Link to="/category/fashion">Fashion</Link></li>
            <li><Link to="/category/home">Home</Link></li>
            <li><Link to="/category/sports">Sports</Link></li>
            <li><Link to="/category/beauty">Beauty</Link></li>
            {/* Add more categories as needed */}
          </ul>
        </div>

        {/* Slideshow Section */}
        <div className="slideshow">
          <a href={images[currentImageIndex].link}>
            <img
              src={images[currentImageIndex].src}
              alt={images[currentImageIndex].alt}
            />
          </a>
        </div>

        {/* Right Links Section */}
        <div className="right-links">
          <Link to="/help-centre">Help Centre</Link>
          <Link to="/easy-return">Easy Return</Link>
          <Link to="/sell-on-jumia">Sell on Jumia</Link>
        </div>
      </div>
      <div className="home">
      
      <Heading heading="Supermarket" className="heading" />
      <div className="home_row">
        {data
          .filter((filrterdData) => filrterdData.category === "Supermarket")
          .slice(0, 5)
          .map((item) => (
            <Product
              id={item.id}
              key={item.id}
              title={item.desc}
              price={item.price}
              rating={item.star}
              image={item.image_url}
            />
          ))}
      </div>

      <Heading heading="Phones and Tablets" className="heading" />
      <div className="home_row">
        {data
          .filter(
            (filrterdData) => filrterdData.category === "Phones and Tablets"
          )
          .slice(0, 5)
          .map((item) => (
            <Product
              id={item.id}
              key={item.id}
              title={item.desc}
              price={item.price}
              rating={item.star}
              image={item.image}
            />
          ))}
      </div>

      <Heading heading="Electronics" className="heading" />
      <div className="home_row">
        {data
          .filter((filrterdData) => filrterdData.category === "Electronics")
          .slice(0, 5)
          .map((item) => (
            <Product
              id={item.id}
              key={item.id}
              title={item.desc}
              price={item.price}
              rating={item.star}
              image={item.image}
            />
          ))}
      </div>

      <Heading heading="Sports" className="heading" />
      <div className="home_row">
        {data
          .filter((filrterdData) => filrterdData.category === "Sports")
          .slice(0, 5)
          .map((item) => (
            <Product
              id={item.id}
              key={item.id}
              title={item.desc}
              price={item.price}
              rating={item.star}
              image={item.image}
            />
          ))}
      </div>

      <Heading heading="Computing" className="heading" />
      <div className="home_row">
        {data
          .filter((filrterdData) => filrterdData.category === "computing")
          .slice(0, 5)
          .map((item) => (
            <Product
              id={item.id}
              key={item.id}
              title={item.desc}
              price={item.price}
              rating={item.star}
              image={item.image}
            />
          ))}
      </div>
      {/* <Footer /> */}
    </div>
    </div>
  );
}


export default SectionBelowHeader
