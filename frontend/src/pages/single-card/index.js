import {
  Container,
  Main,
  Button,
  TagsContainer,
  Icons,
  LinkComponent,
} from "../../components";
import { UserContext, AuthContext } from "../../contexts";
import { useContext, useState, useEffect } from "react";
import styles from "./styles.module.css";
import Ingredients from "./ingredients";
import Description from "./description";
import cn from "classnames";
import { useRouteMatch, useParams, useHistory } from "react-router-dom";
import MetaTags from "react-meta-tags";

import { useRecipe } from "../../utils/index.js";
import api from "../../api";
import Schedule from "./schedule";

const SingleCard = ({ loadItem, updateOrders }) => {
  const [loading, setLoading] = useState(true);
  const { recipe, setRecipe, handleLike, handleAddToCart, handleSubscribe } =
    useRecipe();
  const authContext = useContext(AuthContext);
  const userContext = useContext(UserContext);
  const { id } = useParams();
  const history = useHistory();


  useEffect((_) => {
    api
      .getRecipe({
        recipe_id: id,
      })
      .then((res) => {
        setRecipe(res);
        setLoading(false);
      })
      .catch((err) => {
        history.push("/groups");
      });
  }, []);

  const { url } = useRouteMatch();
  const {
    teacher = {},
    image,
    rubric,
    number_of_lessons,
    name,
    title,
    students,
    description,
    is_joining,
    is_in_students,
    is_staff,
    begin_at,
    schedule_templates,
  } = recipe;

  return (
    <Main>
      <Container>
        <MetaTags>
          <title>
            {name}. {title}
          </title>
          <meta name="description" content={`Продуктовый помощник - ${name}`} />
          <meta property="og:title" content={name} />
        </MetaTags>
        <div className={styles["single-card"]}>
          <img
            src={image}
            alt={name}
            className={styles["single-card__image"]}
          />
          <div className={styles["single-card__info"]}>
            <div className={styles["single-card__header-info"]}>
              <h1 className={styles["single-card__title"]}>{name}</h1>
            </div>
            <TagsContainer tags={rubric} />
            <div>
              <h2 className={styles["single-card__text"]}>{title}</h2>
              <p className={styles["single-card__text"]}>
                <Icons.ClockIcon /> {number_of_lessons} ч.
              </p>
              <p className={styles["single-card__text_with_link"]}>
                <div className={styles["single-card__text"]}>
                  <Icons.UserIcon />{" "}
                  <LinkComponent
                    title={`${teacher.first_name} ${teacher.last_name}`}
                    href={`/user/${teacher.id}`}
                    className={styles["single-card__link"]}
                  />
                </div>
              </p>
            </div>
            <div className={styles["single-card__buttons"]}>
              {authContext && !is_in_students && !is_staff && (
                <Button
                  className={styles["single-card__button"]}
                  modifier={is_joining ? "style_light" : "style_dark-blue"}
                  clickHandler={(_) => {
                    handleAddToCart({
                      id,
                      toAdd: Number(!is_joining),
                      callback: updateOrders,
                    });
                  }}
                >
                  {is_joining ? (
                    <>
                      <Icons.DoneIcon color="#4A61DD" />
                      Заявка подана
                    </>
                  ) : (
                    <>
                      <Icons.PlusIcon /> Подать заявку
                    </>
                  )}
                </Button>
              )}
            </div>
            <Ingredients
              ingredients={
                is_in_students || (userContext || {}).id === teacher.id
                  ? students
                  : ""
              }
            />
            <Description description={description} />
            <div className={styles["single-card__text"]}>
              Начало занятий: {begin_at}
            </div>
            <Schedule items={schedule_templates} />

            <div className={styles["single-card__text"]}>
              {(userContext || {}).id == teacher.id && authContext && (
                <Button
                  className={styles["single-card__button"]}
                  modifier="style_light-blue"
                  href={`${url}/edit`}
                >
                  {"Редактировать группу"}
                </Button>
              )}
              {(userContext || {}).id == teacher.id && authContext && (
                <Button
                  className={styles["single-card__button"]}
                  modifier="style_light-blue"
                  href={`${url}/schedule`}
                >
                  {"Редактировать расписание"}
                </Button>
              )}
              {(userContext || {}).id == teacher.id && authContext && (
                <Button
                  className={styles["single-card__button"]}
                  modifier="style_light-blue"
                  clickHandler={_ => {
                    api.createLessons({group_id: id})
                    .then(res => {history.push(`${url}/diary/`)})
                  }}
                >
                  Сформировать занятия
                </Button>
              )}
            </div>
          </div>
        </div>
      </Container>
    </Main>
  );
};

export default SingleCard;
