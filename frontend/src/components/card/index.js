import styles from './style.module.css'
import { LinkComponent, Icons, Button, TagsContainer } from '../index'
import { useState, useContext } from 'react'
import { AuthContext } from '../../contexts'

const Card = ({
  name = 'Без названия',
  id,
  title,
  image,
  is_joining,
  is_in_students,
  is_teacher,
  is_staff,
  rubric,
  number_of_lessons,
  teacher = {},
  handleLike,
  handleAddToCart,
  updateOrders
}) => {
  const authContext = useContext(AuthContext)
  return <div className={styles.card}>
      <LinkComponent
        className={styles.card__title}
        href={`/groups/${id}`}
        title={<div className={styles.card__image} style={{ backgroundImage: `url(${ image })` }} />}
      />
      <div className={styles.card__body}>
        <LinkComponent
          className={styles.card__title}
          href={`/groups/${id}`}
          title={`${title} ${name}`}
        />

        <TagsContainer tags={rubric} />
        <div className={styles.card__time}>
          <Icons.ClockIcon /> {number_of_lessons} ч.
        </div>
        <div className={styles.card__author}>
          <Icons.UserIcon /> <LinkComponent
            href={`/user/${teacher.id}`}
            title={`${teacher.first_name} ${teacher.last_name}`}
            className={styles.card__link}
          />
        </div>
      </div>
      
      <div className={styles.card__footer}>
          {authContext && !is_staff && <Button
            className={styles.card__add}
            modifier={is_joining ? 'style_light' : 'style_light-blue'}
            clickHandler={_ => {
              handleAddToCart({
                id,
                toAdd: Number(!is_joining),
                callback: updateOrders
              })
            }}
            disabled={!authContext||is_in_students}
          >
            {is_joining ? <><Icons.DoneIcon />Заявка отправлена</> : <><Icons.PlusIcon fill='#4A61DD' /> Подать заявку</>}
          </Button>}
          {authContext && is_teacher ? <p>Вы куратор этой группы</p>: <></>}

      </div>
  </div>
}

export default Card