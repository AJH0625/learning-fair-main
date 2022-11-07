import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import $ from 'jquery';
import { useNavigate } from "react-router-dom";
import "../../css/layouts/header.scss"
$("#nav-1 a").on("click", function() {
  var position = $(this)
    .parent().position();
  var width = $(this)
    .parent().width();
  $("#nav-1 .slide1").css({ opacity: 1, left: +position.left, width: width });
});

$("#nav-1 a").on("mouseover", function() {
  var position = $(this)
    .parent().position();
  var width = $(this)
    .parent().width();
  $("#nav-1 .slide2").css({ 
    opacity: 1, left: +position.left, width: width })
    .addClass("squeeze");
});

$("#nav-1 a").on("mouseout", function() {
  $("#nav-1 .slide2").css({ opacity: 0 }).removeClass("squeeze");
});
var currentWidth = $("#nav-1")
  .find("li:nth-of-type(3) a")
  .parent("li")
  .width();
var current= $("#nav-1").find("li:nth-of-type(3) a").position()
const Header = () => {
  const [current, setCurrent] = useState($(`li:nth-of-type(3) a`).position());
  const navigate = useNavigate();
  function handleOnClick(url,nth){
    navigate(url)
    setCurrent($(`li:nth-of-type(${nth}) a`).position());
  }
  $("#nav-1 .slide1").css({ left: +current.left, width: currentWidth });
  return (
    <header>
      <ul id="nav-1" > 
        <li className="slide1"></li>         
        <li className="slide2"></li>
        {/* <li><a href="/main">Home</a></li>
        <li><a href="/class">Class</a></li>
        <li><a href="/tags">Tags</a></li>
        <li><a href="/congrats">축사</a></li>
        <li><a href="/awards">시상식</a></li> */}
        <li><a onClick={()=>handleOnClick('/main',3)}>Home</a></li>
        <li><a onClick={()=>handleOnClick('/class',4)}>분반</a></li>
        <li><a onClick={()=>handleOnClick('/tags',5)}>Tags</a></li>
        <li><a onClick={()=>handleOnClick('/congrats',6)}>축사</a></li>
        <li><a onClick={()=>handleOnClick('/awards',7)}>시상식</a></li>   
      </ul>
    </header>
  );
}

export default Header