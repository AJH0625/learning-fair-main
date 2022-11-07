import React, { useState } from 'react';
import $ from 'jquery';
import { useNavigate } from "react-router-dom";
import "../../css/layouts/header.scss"
import  Button  from './button';
import  Menu  from './menu';
const Header = () => {
  
  const [userName, setUserName] = useState('방문자');
  const navigate = useNavigate();
  function handleOnClick(url){
    navigate(url)
  }
  const [classURL, setClassURL] = useState('/class');
  var jbRandom = Math.random();
  return (
    <header className="header">
      <img src="skkuLearningFair.png" onClick={()=>handleOnClick('/main')} alt="" className="headerLogo"/>
      <div className="headerMenu">
        <Button className='.button' id='ClassBtn' value='분반'>
          <Menu className="classMenu" onClick={setClassURL} />
        </Button>
        <Button id='TagBtn' onClick={()=>handleOnClick('/tag')} value='해시태그'/>
        <Button id='CongratsBtn' onClick={()=>handleOnClick('/congrats')} value='축사'/>
        <Button id='Awards' onClick={()=>handleOnClick('/awards')} value='시상식'/>
        <Button id='Explore' onClick={()=>handleOnClick(`/project/${Math.floor( jbRandom * 100 ) }`)} value='탐험하기'/>
      </div>  
      <div className="headerWelcome">
        <p><span id="user">{userName}</span>님, 환영합니다!</p>
      </div>
    </header>
  );
}

export default Header