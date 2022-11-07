import { useParams } from 'react-router-dom';
import '../css/Class.css';
function Project() {
    const projectId = useParams().projectId;    
    return (
        <div className="Project">
            {projectId}
        </div>
    );
}

export default Project;
