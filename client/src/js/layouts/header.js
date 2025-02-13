import React, { useState } from 'react';
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
  const [isActive, setActive] = useState(false);
  const handleToggle = () => {
    setActive(!isActive);
  };
  return (
    <header className="header">
      <img src={`${process.env.PUBLIC_URL}/skkuLearningFair.png`} onClick={()=>handleOnClick('/main')} alt="" className="headerLogo"/>
      <div className="headerMenu">
        <Button className='button' onClick={handleToggle} id='ClassBtn' value='분반'>
            <div className={`classMenu ${isActive ? "onclick" : ""}`}>
                <MenuGroup className="leftMenu"> 
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

      <nav id="main-menu">
        <ul>
          <li>
          <Button id='ClassBtn2' onClick={()=>handleOnClick('/class')} value='분반'/>
          </li>
          <li>
          <Button id='TagBtn2' onClick={()=>handleOnClick('/tag')} value='해시태그'/>
          </li>
          <li>
          <Button id='CongratsBtn2' onClick={()=>handleOnClick('/congrats')} value='축사'/>
          </li>
          <li>
          <Button id='Awards2' onClick={()=>handleOnClick('/awards')} value='시상식'/>
          </li>
          <li>
          <Button id='Explore2' onClick={()=>handleOnClick('/project/${Math.floor( jbRandom * 100 ) }')} value='탐험하기'/>
          </li>         
        </ul>
      </nav>
      <input type="checkbox" id="hamburger-input" class="burger-shower"/>
      <label id="hamburger-menu" for="hamburger-input">
        <nav id="sidebar-menu">
          <h3>닫기</h3>
          <ul>
            <li>
              <div class="dropdown">
                <li>
                <Button id='dropbtn' onClick={()=>handleOnClick('/class')} value='분반'/>
                </li>
                
                <ul class="dropdown-content">
                  <li><a href="/class/DASF002I1">DASF002I1</a></li>
                  <li><a href="/class/DASF002I2">DASF002I2</a></li>
                  <li><a href="/class/DASF002I3">DASF002I3</a></li>
                  <li><a href="/class/DASF002I4">DASF002I4</a></li>
                  <li><a href="/class/DASF002I5">DASF002I5</a></li>
                  <li><a href="/class/DASF002I6">DASF002I6</a></li>
                  <li><a href="/class/DASF002I7">DASF002I7</a></li>
                  <li><a href="/class/DASF002I8">DASF002I8</a></li>
                  <li><a href="/class/DASF002I9">DASF002I9</a></li>
                  <li><a href="/class/GEDT015I1">GEDT015I1</a></li>
                </ul>
              </div>
            </li>
              <li>
              <Button id='TagBtn2' onClick={()=>handleOnClick('/tag')} value='해시태그'/>
              </li>    
              <li>
              <Button id='CongratsBtn2' onClick={()=>handleOnClick('/congrats')} value='축사'/>
              </li>
              <li>
              <Button id='Awards2' onClick={()=>handleOnClick('/awards')} value='시상식'/>
              </li>
              <li>
              <Button id='Explore2' onClick={()=>handleOnClick('/project/${Math.floor( jbRandom * 100 ) }')} value='탐험하기'/>
              </li>             
          </ul>
        </nav>
      </label>
      <div class="overlay"></div>
      


      <div className="headerWelcome">
        <p><span id="user">{userName}</span>님, 환영합니다!</p>
      </div>
    </header>
  );
}

export default Header