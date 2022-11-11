import React from "react"
import "../../css/layouts/footer.css"
// import Favicon from "./favicon"
const Footer = () => {
  return (
    <footer>
      <div className="wrapper">
        {/* <div className="img">
          <a href="https://www.skku.edu/skku/index.do"  target='_blank'><img id="footerLogoImg"src="skku.png" alt=""/></a>
        </div> */}
        <div className="copyright">
          {/* <p><a href="https://github.com/2022-Learning-Fair" target='_blank'><Favicon/></a></p> */}
          <p>Copyright ⓒ 2022 Learning Fair, Sungkyunkwan University</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
