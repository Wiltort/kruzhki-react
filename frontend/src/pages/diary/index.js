import { useState, useEffect, useContext } from "react";
import {
  ScheduleForm,
  Container,
  Input,
  Title,
  Textarea,
  Main,
  Button,
} from "../../components";
import api from "../../api";
import styles from "./styles.module.css";
import { useParams, useHistory } from "react-router-dom";
import MetaTags from "react-meta-tags";


const Diary = ({ isStaff }) => {
  const authContext = useContext(AuthContext)
  const userContext = useContext(UserContext)
  const [ user, setUser ] = useState(null)
  const [ students, setStudents ] = useState([])
  const [ lessons, setLessons ] = useState([])
  const [ groups, setGroups ] = useState([])

  const getGroups = () => {
    api
    .getGroups
  }


}

