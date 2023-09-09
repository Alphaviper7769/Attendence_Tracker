import { useEffect, useState } from 'react';
import axios from 'axios';

const Teacher = (props) => {
    const [id, setId] = useState(1);
    const [response, setResponse] = useState([]);
    const [currentCourse, setCurrentCourse] = useState();
    const [date, setDate] = useState(new Date().getTime());
    useEffect(() => {
        const fetch = async () => {
            const data = await axios.get(`http://localhost:5000/teacher/${id}`);
            setResponse(data);
        };
        fetch();
    }, [id]);

    useEffect(() => {
        const change = async () => {
            const data = await axios.get(`http://localhost:5000/teacher/${id}/${currentCourse}/${date}`);
            setResponse(data);
        }
        change();
    }, [id, currentCourse, date]);

    const reduceTime = () => {
        setDate(date - 86400000);
    };

    const increaseTime = () => {
        setDate(date + 86400000);
    };

    let tempId;

    return (
        <div className="teacher-div">
            <div className='id'>
                <input type='text' value={tempId} className='border-black border-2 rounded-md ' />
                <button onClick={() => setId(tempId)}>SUBMIT</button>
            </div>
            <div className='teacher-date'>
                <button onClick={reduceTime}>Yesterday</button>
                <div><section>{new Date(date).getDate()} / {new Date(date).getMonth()} / {new Date(date).getFullYear()}</section></div>
                <button onClick={increaseTime}>Tomorrow</button>
            </div>
            <div className="courses">
                {response.map((res) => {
                    return (
                        <div className='courses-div' onClick={() => setCurrentCourse(res)}>
                            {res}
                        </div>
                    );
                })}
            </div>
            <div className="teacher-main"></div>
        </div>
    );
};

export default Teacher;