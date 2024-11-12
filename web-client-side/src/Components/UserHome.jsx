import React from 'react';
import { useParams } from 'react-router-dom';

export default function UserHome() {

    const { userId } = useParams();

    return (
    <div>
        <h1>Hello {userId} </h1>
    </div>
  )
}
