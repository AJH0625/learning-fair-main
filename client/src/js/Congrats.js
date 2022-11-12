import '../css/Congrats.css';
import axios from "axios";

function Congrats() {
    axios.get('/congrats-videos')
    .then(function (response) {
        console.log(response)
    })
    .catch(function (error) {
        console.log(error);
    });

    return (
        <div className="Congrats">
            <div className="CongratsWrapper">
                <div className="first">
                    <p>총장님</p>
                </div>
                <div className="second">
                    <p>SW융합대학장님</p>
                </div>
                <div className="second">
                    <p>DS교육센터장<br/>/학부대학장님</p>
                </div>
            </div>
        </div>
    );
}

export default Congrats;
