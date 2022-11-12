import Footer from "./footer"
import Header from "./header"
import "../../css/layouts/layout.scss"
import { Route, Routes, useLocation } from "react-router";
import { useEffect, useState } from "react";
import { useNavigate } from 'react-router-dom';
import axios from "axios";
import Main from "../Main";
import Awards from "../Awards";
import Congrats from "../Congrats";
import Tag from "../Tag";
import Class from "../Class";
import Project from "../Project";

const Layout = () => {
  const [title, setTitle] = useState(false);
  const loc = useLocation().pathname;
  useEffect(() => {
    if (loc==='/main'){
      setTitle("")
    }else if (loc==="/tag"){
      setTitle("해시태그")
    }else if (loc==="/awards"){
      setTitle("Awards")
    }else if(loc.length>6 && loc.slice(0,6)==="/class"){
      setTitle(loc.slice(7))
    }else if(loc.length>8 && loc.slice(0,8)==="/project"){
      setTitle("팀명")//바껴야 함 ~~
    }else if(loc==="/congrats"){
      setTitle("축사")
    }
}, [loc]);
  
  //Session 기능 테스트 - 승열
  //Login.js 에서 axios통한 db등록 성공 시 사용자 name을 글로벌 스테이트로 설정 후 여기서 활용해야 할듯..
  const sessionCheckJson={
    name:"손승열"
  }
  const navigate = useNavigate();

  axios.post('/session-check', JSON.stringify(sessionCheckJson), {
    headers: {
      "Content-Type": `application/json`,
    },
  })
  .then(function (response) {
    if(response["data"]["session"] == "deactive") {
      console.log("You need to login in!");
      navigate("/");
    }
  })
  .catch(function (error) {
    console.log(error);
  });

  return (
    <div>
      <Header />
      <div className="Main">
        <div className={`MainTitle ${title ? "": "hidden" }`}>
          <div className="focus">{title}</div>
          <div className="mask">
            <div className="titleText">{title}</div>
          </div>
        </div>
        <div className="MainContent">
          <Routes>
            <Route path="/main" element={<Main/>}/>
            <Route path="/awards" element={<Awards />}/>
            <Route path="/congrats" element={<Congrats />}/>
            <Route path="/tag" element={<Tag />}/>
            <Route path="/class/:classId" element={<Class />}/>
            <Route path="/project/:projectId" element={<Project />}/>
          </Routes>
        </div>
      </div>
      <Footer />
    </div>
  )
}

export default Layout