import React from 'react'
import { useNavigate } from 'react-router-dom'

const Quick_Navigate = () => {
    const navigate = useNavigate();
    const params = new URLSearchParams(window.location.pathname);
    return {
        navigate,
        params
    }
}

export default Quick_Navigate