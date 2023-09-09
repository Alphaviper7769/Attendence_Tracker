import { useEffect, useState } from 'react';
import axios from 'axios';

const Student = (props) => {
    const [response, setResponse] = useState([]);
    const [date, setDate] = useState(new Date().getTime());

    useEffect(() => {
        const change = async () => {
            const data = await axios.get(`http://localhost:5000/student/${1}/${date}`);
            setResponse(data);
        }
        change();
    }, [date]);

    const reduceTime = () => {
        setDate(date - 86400000);
    };

    const increaseTime = () => {
        setDate(date + 86400000);
    };

    return (
        <div className="student-div flex flex-col">
            <div className='student-date flex flex-row'>
                <button onClick={reduceTime}>Yesterday</button>
                <div><section>{new Date(date).getDate()} / {new Date(date).getMonth() +1} / {new Date(date).getFullYear()}</section></div>
                <button onClick={increaseTime}>Tomorrow</button>
            </div>
            <div className="dates">
                {response.map((res) => {
                    return (
                        <div>
                            <section>{res[0]}</section>
                            <section>{res[1]}</section>
                        </div>
                    );
                })}
            </div>
            <div className="teacher-main"></div>
        </div>
    );
};

export default Student;