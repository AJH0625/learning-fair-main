import Footer from "./footer"
import Header from "./header"
import "../../css/layouts/layout.css"

const Layout = (props) => {
  return (
    <div>
      <Header />
         {props.children}
      <Footer />
    </div>
  )
}

export default Layout