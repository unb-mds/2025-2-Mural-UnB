import Carousel from "components/Carousel"

const CarouselSection = () => {
  return (
    <div className="w-full px-6">
      <section className="w-full py-8 bg-base-200 mt-10">
        <div className="container mx-auto px-4">
          <Carousel />
        </div>
      </section>
    </div>
  )
}

export default CarouselSection
