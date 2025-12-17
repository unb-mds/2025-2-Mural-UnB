interface TagsListProps {
  tags: string[]
}

const TagsList = ({ tags }: TagsListProps) => {
  if (!tags || tags.length === 0) return null

  return (
    <div className="flex flex-wrap gap-3 mb-8 pb-8 border-b border-[#e5e5e5]">
      {tags.map((tag) => (
        <span
          key={tag}
          className="inline-block py-2 px-4 bg-[#f0f9f4] border border-[#b8e6d0] rounded-[20px] text-sm text-[#15663e] font-medium"
        >
          {tag.replace(/_/g, " ")}
        </span>
      ))}
    </div>
  )
}

export default TagsList
