import '../css/Class.scss';
import { useParams } from 'react-router-dom';
import Grid from './Grid/Grid';
import axios from "axios";
import { useEffect, useRef, useState } from 'react';

function Class() {
    const classId = useParams().classId;
    const projectList=useRef([]);
    useEffect(() => {
        axios.get('/class-project-list',{
            params: {
                class:classId
            }
        })
        .then(function (response) {
            projectList.current=[]
            response.data.projects.map((project,i)=>{
                projectList.current.push(project)
            })
            console.log(projectList.current)
        })
        .catch(function (error) {
            console.log(error);
        });
    }, []);


    return (
        <div className="Class">
            { projectList.current.map((project)=>{
                    return (<Grid project={project}/>)
                }) 
            }
        </div>
    );
}

export default Class;
