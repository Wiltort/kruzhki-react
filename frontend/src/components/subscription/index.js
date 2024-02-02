import styles from './styles.module.css'
import cn from 'classnames'
import { Icons, Button, LinkComponent } from '../index'
const countForm = (number, titles) => {
  number = Math.abs(number);
  if (Number.isInteger(number)) {
    let cases = [2, 0, 1, 1, 1, 2];  
    return titles[ (number % 100 > 4 && number % 100 < 20) ? 2 : cases[(number%10<5)?number%10:5] ]
  }
  return titles[1];
}

const Subscription = ({ email, first_name, last_name, username, removeSubscription, Groups_count, id, Groups }) => {
  const shouldShowButton = Groups_count  > 3
  const moreGroups = Groups_count - 3
  return <div className={styles.subscription}>
    <div className={styles.subscriptionHeader}>
      <h2 className={styles.subscriptionTitle}>
        <LinkComponent className={styles.subscriptionGroupLink} href={`/user/${id}`} title={`${first_name} ${last_name}`} />
      </h2>
    </div>
    <div className={styles.subscriptionBody}>
      <ul className={styles.subscriptionItems}>
        {Groups.map(Group => {
          return <li className={styles.subscriptionItem} key={Group.id}>
            <LinkComponent className={styles.subscriptionGroupLink} href={`/Groups/${Group.id}`} title={
              <div className={styles.subscriptionGroup}>
                <img src={Group.image} alt={Group.name} className={styles.subscriptionGroupImage} />
                <h3 className={styles.subscriptionGroupTitle}>
                  {Group.name}
                </h3>
                <p className={styles.subscriptionGroupText}>
                  <Icons.ClockIcon />{Group.cooking_time} мин.
                </p>
              </div>
            } />
          </li>
        })}
        {shouldShowButton && <li className={styles.subscriptionMore}>
          <LinkComponent
            className={styles.subscriptionLink}
            title={`Еще ${moreGroups} ${countForm(moreGroups, ['рецепт', 'рецепта', 'рецептов'])}...`}
            href={`/user/${id}`}
          />
        </li>}
      </ul>
    </div>
    <div className={styles.subscriptionFooter}>
      <Button
        className={styles.subscriptionButton}
        clickHandler={_ => {
          removeSubscription({ id })
        }}
      >
        Отписаться
      </Button>
    </div>
  </div>
}

export default Subscription
