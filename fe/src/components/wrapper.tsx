type WrapperProps = {
  children: React.ReactNode
}

export const Wrapper = ({ children }: WrapperProps) => {
  return <div className='max-w-[900px] mx-auto'>{children}</div>
}
