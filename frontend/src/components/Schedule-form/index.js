import ScheduleForm from '../form'
import styles from './styles.module.css'
import cn from 'classnames'

const ScheduleForm = ({ loggedIn, children, className, onSubmit }) => {
  return <form
    className={cn(styles.form, className)}
    onSubmit={onSubmit}
  >
    {children}
  </form>
}

export default ScheduleForm
