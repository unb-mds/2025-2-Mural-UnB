import Carousel from "components/Carousel"

const CarouselSection = () => {
  return (
    <div className="w-full px-4 sm:px-6">
      <section className="w-full max-w-5xl mx-auto py-4 sm:py-8 md:py-10 bg-base-200 mt-4 rounded-2xl">
        <div className="px-2 sm:px-4">
          <Carousel />
        </div>
      </section>
    </div>
  )
}

export default CarouselSection
