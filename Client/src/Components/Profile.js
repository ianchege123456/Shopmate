import React, { useEffect, useState } from "react";
import axios from "axios";

function MyAccount() {
  const [userData, setUserData] = useState({});

  useEffect(() => {
    const fetchUserData = async () => {
      const token = localStorage.getItem("token");
      const response = await axios.get("/profile", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setUserData(response.data);
    };

    fetchUserData();
  }, []);

  return (
    <div className="myAccount">
      <h2>My Account</h2>
      <p>Email: {userData.email}</p>
      <p>Name: {userData.name}</p>
      
      {/* Display more user info */}
    </div>
  );
}

export default MyAccount;
