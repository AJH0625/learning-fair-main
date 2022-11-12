import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import '../css/Project.css';
import axios from "axios";
import YouTube from 'react-youtube';

function Project() {
    
    const [project, setProject] = useState({
            class_name:"",team_number:"",team_name:"",team_member:""
            ,project_name:"",project_pdf_url:"",project_youtube_url:""
            ,hashtag_main:"",hashtag_custom_a:"",hashtag_custom_b:"",hashtag_custom_c:""
            ,like_cnt:""
        });
    const [like, setLike] = useState(0);
    const [click, setClick] = useState(false);
    async function project_info_api(projectInfoReqJson){
        try {
            const response = await axios.post('/project-info', 
            JSON.stringify(projectInfoReqJson), {
                    headers: {
                        "Content-Type": `application/json`,
                    },
                })
            const data=response.data
            setProject({
                class_name:data.class_name,
                team_number:data.team_number,
                team_name:data.team_name,
                team_member:data.team_member,
                project_name:data.project_name,
                project_pdf_url:data.project_pdf_url,
                project_youtube_url:(data.project_youtube_url).slice(-11),
                hashtag_main:data.hashtag_main,
                hashtag_custom_a:data.hashtag_custom_a,
                hashtag_custom_b:data.hashtag_custom_b,
                hashtag_custom_c:data.hashtag_custom_c,
                like_cnt:data.like_cnt
            })
            setLike(()=>{return project.like_cnt})
        } catch(e) {
            console.log(e);
        }
    }

    async function handleOnclick(){
        try {
            const response = await axios.get(`/project/${project_id}/like/`, 
                JSON.stringify(), {
                    headers: {
                        "Content-Type": `application/json`,
                    },
                })
            const like_cnt=response.data.like_cnt;
            setLike(like_cnt)
            console.log(click,like_cnt,like)
            setClick(!click)
        } catch(e) {
            console.log(e);
        }
    }

    const project_id = useParams().projectId;   
    useEffect(() => {
        project_info_api({project_id});
        setLike(project.like_cnt)
    }, [project_id]);

    return (
        <div className="Project">
            <div id='ProjectInfo'>
                <button id="like" onClick={handleOnclick}>{like}</button>
                <p id="member">{project.team_member}</p>
                <p id="hashtag">#{project.hashtag_main} #{project.hashtag_custom_a} #{project.hashtag_custom_b} #{project.hashtag_custom_c} </p>
            </div>
            <div className="ProjectContentWrapper">
                <div className="ProjectContent" id="ProjectYoutube">
                    <p>YouTube</p>
                    <YouTube  className="ProjectYoutube" videoId={"fEtJDkaBqyA"}
                        opts={{ 
                                playerVars: { autoplay: 1,rel: 0, modestbranding: 1 },
                            }} 
                        onEnd={(e)=>{e.target.stopVideo(0);}}
                    />
                </div>
                <div className="ProjectContent" id="ProjectPDF">
                    <p>PDF</p>
                    <embed className="ProjectPDF" src={project.project_pdf_url} type="application/pdf"/>
                </div>
            </div>
           
        </div>
    );
}

export default Project;
