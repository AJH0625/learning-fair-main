import '../css/Class.scss';
import { useParams } from 'react-router-dom';
import Grid from './Grid/Grid';
import axios from "axios";
import { useEffect, useRef, useState } from 'react';

function Class() {
    const classId = useParams().classId;
    const [projects, setprojects] = useState([]);
    const projectList=useRef(projects);
    axios.get('/class',{
        params: {class:classId}
    })
    .then(function (response) {
        setprojects(response.data.projects)
    })
    .catch(function (error) {
        console.log(error);
    });
    useEffect(() => {
        projectList.current = projects; 
     },[projects]) 

    return (
        <div className="Class">
            { projectList.current.map((project)=>{
                    return (<Grid project={project} key={project.project_id}/>)
                }) 
            }
        </div>
    );
}

export default Class;
