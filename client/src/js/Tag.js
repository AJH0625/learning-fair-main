import { useParams } from 'react-router-dom';
import '../css/Tag.css';
function Tag() {
    const tagId = useParams().tagId;    
    return (
        <div className="Tag">
        </div>
    );
}

export default Tag;
