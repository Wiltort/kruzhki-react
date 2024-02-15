import styles from './styles.module.css'
import cn from 'classnames'
import { Tag } from '../index'

const TagsContainer = ({ tags }) => {
  if (!tags) { return null }
  return <div className={styles['tags-container']}>
    {tags.map(rubric => {
      return <Tag
        key={rubric.id}
        color={rubric.color}
        name={rubric.name}
      />
    })}
  </div>
}

export default TagsContainer