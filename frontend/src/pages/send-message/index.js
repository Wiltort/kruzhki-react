import {
  Container,
  Input,
  Title,
  Main,
  Form,
  Button,
  Textarea,
} from "../../components";
import styles from "./styles.module.css";
import api from "../../api";
import { useEffect, useState } from "react";
import { useHistory, useParams } from "react-router-dom";
import MetaTags from "react-meta-tags";



const SendMessage = ({ }) => {
  const [topic, setTopic] = useState("");
  const history = useHistory();
  const { id } = useParams();
  const [messageText, setMessageText] = useState("");
  const [ User, setUser ] = useState()

  const getUser = (id) => {
    api.getUser({id: id})
      .then(res => {
        setUser(res)
      })
  }

  const checkIfDisabled = () => {
    return (
      topic === "" ||
      messageText === "" 
    );
  };

  useEffect(_ => {
    getUser(id)
  }, [])

  return (
    <Main>
      <Container>
        <MetaTags>
          <title>Отправка сообщения</title>
          <meta
            name="description"
            content="Кружки - Отправка сообщения"
          />
          <meta property="og:title" content="Отправка сообщения" />
        </MetaTags>
        <Title title={`Отправка сообщения пользователю ${User? `${User.first_name} ${User.last_name}`:""}`} />
        <Form
          className={styles.form}
          onSubmit={(e) => {
            e.preventDefault();
            const data = {
              user_id: id,
              topic: topic,
              text: messageText,
            };
            api
              .sendMessage(data)
              .then((res) => {
                history.push(`/user/${id}`);
              })
              .catch((err) => {
                const { non_field_errors} = err;
                if (non_field_errors) {
                  return alert(non_field_errors.join(", "));
                }
                const errors = Object.values(err);
                if (errors) {
                  alert(errors.join(", "));
                }
              });
          }}
        >
          <Input
            label="Тема сообщения"
            onChange={(e) => {
              const value = e.target.value;
              setTopic(value);
            }}
          />
          <Textarea
            label="Текст сообщения"
            onChange={(e) => {
              const value = e.target.value;
              setMessageText(value);
            }}
          />
          <Button
            modifier="style_dark-blue"
            disabled={checkIfDisabled()}
            className={styles.button}
          >
            Отправить
          </Button>
        </Form>
      </Container>
    </Main>
  );
};

export default SendMessage;
