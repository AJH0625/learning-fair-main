import '../css/Login.css';
import Radio from "./login/Radio";
import RadioGroup from './login/RadioGroup';
import { useState } from "react";
import InputTextGroup from './login/InputTextGroup';
import InputText from './login/InputText';
import { useNavigate } from 'react-router-dom';
import axios from "axios";

function Login() {
  const navigate = useNavigate();

  const [radioValue,setRadioValue]=useState("재학생")
  const [isShow, setShow] = useState(true)
  const [name,setName]=useState("")
  const [studentId,setStudentId]=useState("")
  const [major,setMajor]=useState("")

  const handleName = ({ target: { value } }) => setName(value);
  const handleStudentId = ({ target: { value } }) => setStudentId(value);
  const handleMajor = ({ target: { value } }) => setMajor(value);

  function onClickStudent(){
    setShow(true);
    setName("")
    setStudentId("")
    setMajor("")
  }
  function onClickOther(){
    setShow(false);
    setName("")
    setStudentId("")
    setMajor("")
  }

  async function login_api(submitValue){
    try {
        const response = await axios.post('/login', JSON.stringify(submitValue), {
          headers: {
            "Content-Type": `application/json`,
          },
        })

        console.log(response);
        localStorage.setItem('login-token',response.data.token)
        navigate("/main");
    } catch(e) {
      console.log(e);
    }
  }

  function handleLoginBtn(){
    if (name.length<2){
      alert('이름을 정확히 입력해주세요!')
      setName("")
      return
    }
    if (radioValue==='재학생'){
      if (studentId.length!==10 || isNaN(studentId)){
        console.log(studentId)
        alert('학번을 정확히 입력해주세요!')
        setStudentId("")
        return
      }
      if (major.length<2){
        alert('학과를 정확히 입력해주세요!')
        setMajor("")
        return
      }
    }
    else{
      setStudentId(0)
      setMajor(radioValue)
    }
    const submitValue={
      userType:radioValue,
      name,
      studentId,
      major
    }

    login_api(submitValue);

    /*
    axios.post('/login', JSON.stringify(submitValue), {
      headers: {
        "Content-Type": `application/json`,
      },
    })
    .then(function (response) {
      console.log(response);
      navigate("/main");
    })
    .catch(function (error) {
      console.log(error);
    });
    */


    //navigate("/main");
    //console.log(submitValue)
  }

  return (
    <div className="Login">
      <center>
        <div className="loginHeader">
          <p>2022</p>
          <p>Learning Fair</p>
          <p>문제해결과알고리즘</p>
        </div>
        <div className="loginBody">
          <div className="loginBody-top">
            <div className="logoText">
              <p>sungkyunkwan university</p>
              <p>11.23-12.04</p>
            </div>
            <img src={`${process.env.PUBLIC_URL}/skku.png`} className="logoImg" alt="skku.png"/>
          </div>
          <div className="loginBody-middle">
            <form>
              <RadioGroup value={radioValue} onChange={setRadioValue} >
                <Radio id="radioStudent" value="재학생" onClick={onClickStudent}/>
                <Radio id="radioOther" value="외부인" onClick={onClickOther} />
              </RadioGroup>
              <InputTextGroup className="inputText" show={isShow}>
                {isShow&&<InputText id="inputStudent" nameValue={name} onNameChange={handleName} studentIdValue={studentId} onStudentIdChange={handleStudentId} majorValue={major} onMajorChange={handleMajor}/>}
                {!isShow&&<InputText id="inputOther" nameValue={name} onNameChange={handleName} />}
              </InputTextGroup>
            </form>
          </div>
          <div className="loginBody-base">
            <p>learing fair'22</p>
          </div>
        </div>
        <div className="loginButton" type="submit" onClick={handleLoginBtn}>
          <span>enter to the wave</span>
          <div className="dot"></div>
        </div>
      </center>
  </div>
  );
}

export default Login;
