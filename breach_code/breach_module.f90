module breach_module

    implicit none
    save

    logical, private :: module_setup = .false.

    ! Place data here
    real(kind=8) :: mu, sigma, lat0, lat1, lon0, lon1, start_time, end_time, time_ratio, breach_trigger, data

contains

    subroutine setup_breaching(path)

        implicit none

        ! Input
        character(len=*), optional, intent(in) :: path

        ! Locals
        integer, parameter :: unit = 54
        character(len=128) :: line


        if (.not.module_setup) then

            ! Open data file
            if (present(path)) then
                open(unit, file = path)
            else
                open(unit, file = 'breach.data')
            endif

            ! Basic switch to turn on variable friction
            read(unit, *)
            read(unit, *) breach_trigger
            read(unit, *) lat0
            read(unit, *) lat1
            read(unit, *) lon0
            read(unit, *) lon1
            read(unit, *) mu
            read(unit, *) sigma
            read(unit, *) time_ratio
            read(unit, *) start_time
            read(unit, *) end_time
            close(unit)
            print *, mu, lat0
            module_setup = .true.
        end if

    end subroutine setup_breaching

    subroutine some_other_routine()

        implicit none

        ! Do stuff - maybe call from b4step


    end subroutine some_other_routine


end module breach_module
