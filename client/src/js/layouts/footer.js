import React from "react"
import "../../css/layouts/footer.css"
const Footer = () => {
  return (
    <footer>
      <div className="wrapper">
        <div className="img">
          <a href="."><img src="di.png" alt=""/></a>
        </div>
        <div className="copyright">
          <p>Copyright ⓒ 2022-2023 DIHYEOKGONG, Sungkyunkwan University</p>
          <p>서울특별시 종로구 성균관로 25-2</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
