import '../css/Class.css';
import { useParams } from 'react-router-dom';
import Grid from './Grid/Grid';
import axios from "axios";
import { useEffect, useState } from 'react';

function Class() {
    const classId = useParams().classId;
    
    useEffect(() => {
        axios.get('/class-project-list',{
            params: {
                class:classId
            }
        })
        .then(function (response) {
            console.log(response)
        })
        .catch(function (error) {
            console.log(error);
        });
    }, []);


    return (
        <div className="Class">
            <Grid/><Grid/><Grid/>
            <Grid/><Grid/><Grid/>
        </div>
    );
}

export default Class;
