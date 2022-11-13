import { useEffect, useState } from 'react';
import { useLocation, useParams } from 'react-router-dom';
import '../css/Project.scss';
import axios from "axios";
import YouTube from 'react-youtube';
import { useRef } from 'react';

function Project() {
    
    const project=useRef("")
    // const like=useRef(0)
    const [like_show, setLike] = useState(0);
    const click=useRef(false)

    async function project_info_api(projectInfoReqJson){
        try {
            const response = await axios.post('/project-info', 
            JSON.stringify(projectInfoReqJson), {
                    headers: {
                        "Content-Type": `application/json`,
                    },
                })
            const data=response.data
            project.current={
                class_name:data.class_name,
                team_number:data.team_number,
                team_name:data.team_name,

                project_name:data.project_name,
                team_member:data.team_member,
                
                project_pdf_url:data.project_pdf_url,
                project_youtube_url:(data.project_youtube_url).slice(-11),
                
                hashtag_main:data.hashtag_main,
                hashtag_custom_a:data.hashtag_custom_a,
                hashtag_custom_b:data.hashtag_custom_b,
                hashtag_custom_c:data.hashtag_custom_c,
                
                like_cnt:data.like_cnt
            }
            // like.current=project.current.like_cnt
            setLike(project.current.like_cnt)
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
            if (like_show>response.data.like_cnt){
                click.current=false
            }else{
                click.current=true
            }
            // console.log("click",click.current,like.current,response.data.like_cnt)
            // like.current=response.data.like_cnt
            setLike(response.data.like_cnt)
        } catch(e) {
            console.log(e);
        }
    }

    const project_id = useParams().projectId;   
    useEffect(() => {
        project_info_api({project_id});
        click.current=false
    }, [project_id]);
    return (
        <div className="Project">
            <div className='ProjectInfo'>
                <h2>{project.current.project_name}</h2>
                <p id="ProjectMember">{project.current.team_member}</p>
                <div class="ProjectInfoWrapper">
                    <button id="ProjectLike" onClick={handleOnclick} className={`${click.current?"":"NoneClick"}`}>
                        <div>
                            <span class="material-symbols-outlined">favorite</span>
                            {like_show}
                        </div>
                    </button>
                    <p id="ProjectHashtag">
                        <span>#{project.current.hashtag_main}</span>
                        <span>#{project.current.hashtag_custom_a}</span>
                        <span>#{project.current.hashtag_custom_b}</span>
                        <span>#{project.current.hashtag_custom_c}</span>
                    </p>
                </div>
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
                    <embed className="ProjectPDF" src={project.current.project_pdf_url} type="application/pdf"/>
                </div>
            </div>
           
        </div>
    );
}

export default Project;
