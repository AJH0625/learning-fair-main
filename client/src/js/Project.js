// import { Axios } from 'axios';
import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import '../css/Project.css';
function Project() {
    const projectId = useParams().projectId;   

    //변수명 db에 맞게 바꿔주시면 됩니다
    const [inputData, setInputData] = useState([{
        className: '',
        members: '',
        pdf: '',
        like: '',
        youtubeURL:'',
        hashtags:''
        //더 있나 혹쉬 
    }])
    
    // useEffect(async() => {
    //     try{
    //         // const res = await Axios.get('/api/test/{}')
    //         // const _inputData = await res.data~~~~
    //         // setInputData(_inputData)
    //     } catch(e){
    //         console.error(e.message)
    //     }
    // },[])
 
    //더미데이터 
    const members=['김보민','장지원','손승열','안정후'];
    const className='DASF002I5';
    const pdf='./ppt.pdt'  
    const like='51';
    const youtubeURL='https://youtu.be/ft9FP_8BLjI';
    const hashtags=['2','1','3','4'];

    return (
        <div className="Project">
            
        </div>
    );
}

export default Project;
