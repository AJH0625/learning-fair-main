import '../css/Congrats.css';
import axios from "axios";
import { useEffect, useState } from 'react';

function Congrats() {
    const [URLs, setURLs] = useState("");
   
    useEffect(() => {
        axios.get('/congrats-videos')
        .then(function (response) {
            setURLs(response.data)
            console.log(response.data)
        })
        .catch(function (error) {
            console.log(error);
        });
    }, []);

    return (
        <div className="Congrats">
            <div className="CongratsWrapper">
                <div className="first">
                    <p>총장님</p>
                    <embed type="video/webm" src={URLs.sw_dean} width="500" height="250"/>
                </div>
                <div className="second">
                    <p  id="sw">SW융합대학장님</p>
                    <embed type="video/webm" src={URLs.president} width="450" height="250"/>
                </div>
                <div className="second">
                    <p>DS교육센터장<br/>/학부대학장님</p>
                    <embed type="video/webm" src={URLs.ds_dean} width="450" height="250"/>
                </div>
            </div>
        </div>
    );
}

export default Congrats;
