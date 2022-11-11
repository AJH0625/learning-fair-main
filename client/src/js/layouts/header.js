import React, { useState } from 'react';
// import $ from 'jquery';
import { useNavigate } from "react-router-dom";
import "../../css/layouts/header.scss"
import Button from './header/button';
import MenuGroup from './header/MenuGroup';
import Menu from './header/Menu';

const Header = () => {
  const [userName, setUserName] = useState('방문자');
  const navigate = useNavigate();
  function handleOnClick(classURL){
    navigate(classURL)
  }
  var jbRandom = Math.random();
  const [isActive, setActive] = useState("false");
  const handleToggle = () => {
    setActive(!isActive);
  };
  return (
    <header className="header">
      <img src="skkuLearningFair.png" onClick={()=>handleOnClick('/main')} alt="" className="headerLogo"/>
      <div className="headerMenu">
        <Button className='button' onClick={handleToggle} id='ClassBtn' value='분반'>
            <div className={`classMenu ${isActive ? "onclick" : ""}`}>
                <MenuGroup className="leftMenu" > 
                    <Menu value="DASF002I1"/>
                    <Menu value="DASF002I2"/>
                    <Menu value="DASF002I3"/>
                    <Menu value="DASF002I4"/>
                    <Menu value="DASF002I5"/>
                </MenuGroup>
                <MenuGroup className="rightMenu" >
                    <Menu value="DASF002I6"/>
                    <Menu value="DASF002I7"/>
                    <Menu value="DASF002I8"/>
                    <Menu value="DASF002I9"/>
                    <Menu value="GEDT015I1"/>
                </MenuGroup>
            </div>
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