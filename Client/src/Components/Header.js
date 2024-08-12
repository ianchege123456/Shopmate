import React, { useState } from 'react'
import "./Header.css"

import { Link } from 'react-router-dom'
import { useNavigate } from 'react-router-dom';
import { actionTypes } from "../ContextAPI/Reducer";
import { useStateValue } from "../ContextAPI/StateProvider";
import AccountCircleOutlinedIcon from '@mui/icons-material/AccountCircleOutlined';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import axios from "axios";
import SearchIcon from '@mui/icons-material/Search';



function Header() {
    const [input, setInput] = useState("");
    const navigate = useNavigate();
    const [{ basket, user }, dispatch] = useStateValue();
    const [dropdownVisible, setDropdownVisible] = useState(false);
  
    const toggleDropdown = () => {
      setDropdownVisible(!dropdownVisible);
    };
    

   

    const auth = async () => {
        if (user) {
          try {
            await axios.post('http://127.0.0.1:5000//login');
            dispatch({
              type: 'SET_USER',
              user: null,
            });
          } catch (error) {
            console.error("Error logging out", error);
          }
        }
      };
    

    //SEARCH
  function search(e) {
    e.preventDefault();

    dispatch({
      type: actionTypes.SET_SEARCH_TERM,
      term: input,
    });

    navigate("/search");
  }
  
    return (
    <nav className="header">
        <Link to="/">
            <img className="header__logo" src="/Shopmate .png"alt="Logo" />       
        </Link>

        {/*Searchbar*/}
        <form action='' className='header__search'>
            <div className="header__search">
            <SearchIcon className='header__searchIcon' />
            <input value={input} onChange={(e) => setInput(e.currentTarget.value.toLowerCase())} type='text' placeholder="Search products, brands and categories" className='header__searchInput'/>
        </div>    
            {!input ? (
            ""
            ) : (
            <button
                type="submit"
                onClick={search}
                className="search_button"
            >
                SEARCH{" "}
            </button>
            )}
        </form>
        
        
        {/*3links*/}        
        
        <div className="header__nav">
        
        <div className="header__navItem" onMouseEnter={toggleDropdown} onMouseLeave={toggleDropdown}>
          <div className="header__option">
            <AccountCircleOutlinedIcon />
            <span className="header__optionText">Account</span>
          </div>
          {dropdownVisible && (
            <div className="header__dropdown">
              <Link to="/login">
                <div className="header__dropdownOption">Sign In</div>
              </Link>
              <Link to="/profile">
                <div className="header__dropdownOption">My Account</div>
              </Link>
              <Link to="/orders">
                <div className="header__dropdownOption">Orders</div>
              </Link>
              <Link to="/saveditems">
                <div className="header__dropdownOption">Saved Items</div>
              </Link>
            </div>
          )}
        
            
            <Link to="/help" className='header__link'>
                <div className="header__option">
                    <HelpOutlineIcon className="header__optionLineOne" />
                    <span className="header__optionLineTwo">Help</span>
                </div>
            </Link>
            <Link to="/checkout" className='header__link'>
              <div className="header__optionBasket">
                <ShoppingCartIcon />
                <span className="header__basketCount">
                  {basket?.length}
                </span>
              </div>
            </Link>
          </div>
        </div>
    </nav>
  )
}

export default Header