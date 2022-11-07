import { useContext } from "react";
import ClassURLContext from "./ClassURLContext";

function Menu({id, value, onClick}) {
    const classURL=useContext(ClassURLContext)
    return (
      <div className="classMenu">
        <div className="leftMenu">
            <p value="1">DAS-F002-I1</p>
            <p value="2">DAS-F002-I2</p>
            <p value="3">DAS-F002-I3</p>
            <p value="4">DAS-F002-I4</p>
            <p value="5">DAS-F002-I5</p>
        </div>
        <div className="rightMenu">
            <p value="6">DAS-F002-I6</p>
            <p value="7">DAS-F002-I7</p>
            <p value="8">DAS-F002-I8</p>
            <p value="9">DAS-F002-I9</p>
            <p value="10">GED-T015-I1</p>
        </div>
      </div>
    );
  }
  export default Menu;
  