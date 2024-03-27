import {
  Title,
  Pagination,
  Container,
  Main,
  LinkComponent,
  Button,
} from "../../components";
import { useSubscriptions } from "../../utils";
import api from "../../api";
import { useEffect, useState } from "react";
import MetaTags from "react-meta-tags";
import styles from "./styles.modules.css";

const NotificationsPage = ({ isStaff, updateOrders }) => {
  const [messages, setMessages] = useState([]);
  const [messagesCount, setMessagesCount] = useState(0);
  const [messagesPage, setMessagesPage] = useState(1);
  const [user, setUser] = useState(null);
  const [joinings, setJoinings] = useState([]);

  const getMessages = ({ page }) => {
    api.getMessages({ page }).then((res) => {
      setMessages(res.results);
      setMessagesCount(res.count);
    });
  };

  const handleAccept = ({ id }) => {
    api
      .acceptJoining({ id })
      .then((res) => {
        const joiningsUpd = joinings.filter((jng) => jng.id !== id);
        setJoinings(joiningsUpd);
        updateOrders()
      })
      .catch((err) => {
        const { errors } = err;
        if (errors) {
          alert(errors);
        }
      });
  };

  const handleReject = ({ id }) => {
    api
      .rejectJoining({ id })
      .then((res) => {
        const joiningsUpd = joinings.filter((jng) => jng.id !== id);
        setJoinings(joiningsUpd);
        updateOrders()
      })
      .catch((err) => {
        const { errors } = err;
        if (errors) {
          alert(errors);
        }
      });
  };

  useEffect((_) => {
    if (!isStaff){return}
    api.getJoinings().then((res) => {
      setJoinings(res);
    });
  }, []);

  useEffect(
    (_) => {
      getMessages({ page: messagesPage });
    },
    [messagesPage]
  );

  useEffect((_) => {
    api.getUserData().then((res) => {
      setUser(res);
    });
  }, []);

  return (
    <Main>
      <Container>
        <MetaTags>
          <title>Уведомления</title>
          <meta name="description" content="Кружки - Уведомления" />
          <meta property="og:title" content="Уведомления" />
        </MetaTags>
        <Title title="Уведомления" />
        {isStaff && (
          <div className={styles.messageslist}>
            <div className="messageslisthead">
              Заявки на вступление в группы: {joinings==[]? '': 'заявок нет'}
            </div>
            
            {joinings.map((jng) => (
              <div key={jng.id} className="message">
                <div className="messagetopic">
                  Заявка в группу: {jng.group.name} {jng.group.title}
                </div>
                <div className="messagehead">
                  От:{" "}
                  <LinkComponent
                    href={`user/${jng.user.id}`}
                    title={`${jng.user.first_name} ${jng.user.last_name}`}
                  />
                </div>
                <div className="messagetext">
                  <Button
                    className={styles["single-card__button"]}
                    modifier="style_light-blue"
                    clickHandler={_ => {
                      handleAccept({ id: jng.id });
                    }}
                  >
                    Принять заявку
                  </Button>
                  <Button
                    className={styles["single-card__button"]}
                    modifier="style_light-blue"
                    clickHandler={_ => {
                      handleReject({ id: jng.id });
                    }}
                  >
                    Отклонить заявку
                  </Button>
                </div>
                <div className="messagedate">Получено: {jng.date}</div>
              </div>
            ))}
          </div>
        )}

        <div className={styles.messageslist}>
          <div className="messageslisthead">Сообщения:</div>
          {messages.map((msg) => (
            <div key={msg.id} className="message">
              <div className="messagetopic">Тема: {msg.topic}</div>
              <div className="messagehead">
                Отправитель:{" "}
                <LinkComponent
                  href={`user/${msg.sender.id}`}
                  title={`${msg.sender.first_name} ${msg.sender.last_name}`}
                />
              </div>
              <div className="messagetext">{msg.text}</div>
              <div className="messagedate">Получено: {msg.date}</div>
            </div>
          ))}
        </div>
        <Pagination
          count={messagesCount}
          limit={6}
          onPageChange={(page) => {
            setMessagesPage(page);
          }}
        />
      </Container>
    </Main>
  );
};

export default NotificationsPage;
