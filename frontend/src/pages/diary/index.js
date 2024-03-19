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
  //const [ user, setUser ] = useState(null)
  const [ students, setStudents ] = useState([])
  const [ lessons, setLessons ] = useState([])
  const [ groups, setGroups ] = useState([])
  const [ group_id, setGroup_id ] = useState(null)
  const [ selected, setSelected ] = useState(false)

  const getGroups = () => {
    api
    .getGroups()
    .then(res => {
      setGroups(res)
    })
  }

  const getLessons = ({group_id, isStaff}) => {
    if (isStaff) {
      api.getAttendings({id: group_id})
      .then(res => {
        setStudents(res.students)
        setLessons(res.lessons)
      })
    }
  }

  useEffect(_ => {
    getGroups()
  }, [])

  useEffect(_ => {
    if (!selected) {return}
    getLessons({group_id: group_id, isStaff: isStaff})
  }, [])


}

