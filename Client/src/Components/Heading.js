import React from "react";
import "../Components/Heading.css";

function Heading({ heading }) {
  return (
    <div className="heading">
      <h5>{heading}</h5>
    </div>
  );
}

export default Heading;