import Footer from "./footer"
import Header from "./header"
import "../../css/layouts/layout.scss"
import { useLocation } from "react-router";
import { useEffect, useState } from "react";

const Layout = (props) => {
  const [title, setTitle] = useState(false);
  const loc = useLocation().pathname;
  useEffect(() => {
    if (loc==='/main'){
      setTitle("")
    }else if (loc==="/tag"){
      setTitle("해시태그 모아보기")
    }else if (loc==="/awards"){
      setTitle("시상식 페이지")
    }else if(loc.length>6 && loc.slice(0,6)==="/class"){
      setTitle(loc.slice(7))
    }else if(loc.length>8 && loc.slice(0,8)==="/project"){
      setTitle("팀명")//바껴야 함 ~~
    }else if(loc==="/congrats"){
      setTitle("축사")
    }
}, [loc]);
  
  return (
    <div>
      <Header />
        <div className={`titleWrapper ${title ? "": "hidden" }`}>
          <div className="focus">{title}</div>
          <div className="mask">
            <div className="titleText">{title}</div>
          </div>
        </div>
        <div className="Main">
          {props.children}
        </div>
      <Footer />
    </div>
  )
}

export default Layout