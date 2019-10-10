program barrier_breach ! (maux,mbc,mx,my,xlower,ylower,dx,dy,t,dt,aux)
implicit none

! Allocate variables
! Subroutine variables imported from b4step2.f90
integer :: mbc,maux ! , intent(inout)
integer :: mx, my !, intent(inout)
real(kind=8) ::  t, dt ! , intent(inout)
real(kind=8) :: xlower, ylower, dx, dy, db, depth !, intent(inout) ::
real(kind=8), allocatable, dimension(:) :: x, y, b, xx, yy, bb! , intent(out)

!real(kind=8) :: aux(maux,1-mbc:mx+mbc,1-mbc:my+mbc) ! , intent(inout)

! Local variables



real(kind=8),allocatable, dimension(:,:) :: X_mesh, Y_mesh, B_mesh, XXM, YYM, BBM, breach, bathy

CHARACTER(*), PARAMETER :: fileplace = "/home/claw/clawpack-v5.5.0/geoclaw/scratch/"

mbc = 2
my = 2880 ! number of columns of bathy
mx = 3480 ! number of rows of bathy
dx = 8.33622785689400e-03 ! increments of x
dy = 8.335728657656000e-03 ! increments of y
xlower = -99
ylower = 8
depth = -5000.0
db = abs(depth / (my - 1))
allocate(x(1-mbc:mx+mbc))
call create_bathy(xlower, ylower, mx, my, x, y, dx, dy, b, db, depth, mbc, xx, yy,bb)

!call test_bathy(x,y,b, xx, yy,bb)
call create_grid(X_mesh, Y_mesh, B_mesh, x, y, b, XXM, YYM, BBM)
call test_grid(X_mesh, Y_mesh, B_mesh, XXM, YYM, BBM)
!call create_island(B_mesh, Y_mesh, bathy)
!
!call test_island(bathy)
!call create_breach(X_mesh, Y_mesh, bathy, t)
!call test_breach(breach)

! Initialize breach to match the original bathymetry
!breach(:,:) = aux(1, :, :)

contains
    subroutine create_bathy(xlower, ylower, mx, my, x, y, dx, dy, b, db, depth, mbc, xx, yy,bb)
    implicit none
  ! Subroutine variables
  ! Subroutine variables imported from b4step2.f90
    integer, intent(inout) :: mx, my, mbc
    real(kind=8), intent(inout) :: xlower, ylower, dx, dy, db, depth
    real(kind=8), allocatable, dimension(:), intent(inout) :: y, b, xx, yy, bb
    real(kind=8), dimension(1-mbc:), intent(inout) :: x
    integer :: i, j
    real(kind=8) :: xll, yll, bll
    ! fill x and y like np.linspace
!    allocate(x(1-mbc:mx+mbc))
    allocate(y(1-mbc:my+mbc))
    allocate(b(1-mbc:my+mbc))
    allocate(xx(1-mbc:mx+mbc))
    allocate(yy(1-mbc:my+mbc))
    allocate(bb(1-mbc:my+mbc))
    x = (/((i-0.5d0)*dx + xlower, i=1-mbc,mx+mbc)/)
    y = (/((i-0.5d0)*dy + ylower, i=1-mbc,my+mbc)/)
    b = (/((i-0.5d0)*db + depth, i=1-mbc,my+mbc)/)
!    print *, db, depth
!     do i = 1, size(b)
!       print *, b(i)
!     end do

    do j=1-mbc,my+mbc
        yll = ylower + (j-0.5d0) * dy
        do i=1-mbc,mx+mbc
            xll = xlower + (i-0.5d0) * dx
            bll = depth + (j-0.5d0)*db
            ! Location logic
!            aux(1, i, j) = something
            xx(i) = xll
            yy(j) = yll
            bb(j) = bll
        end do
    end do
  end subroutine create_bathy

    subroutine test_bathy(x, y, b, xx, yy,bb)
        real(kind=8), intent(in), dimension(:) :: x, y, b
        real(kind=8), intent(in), dimension(:) :: xx, yy, bb
!        real, allocatable, dimension(:) ::  bb

        integer :: i, j

!        open(1, File='x_array.txt', form='unformatted')
!        open(2, File='y_array.txt', form='unformatted')
!        open(3, File='b_array.txt', form='unformatted')
!        allocate(xx(3480))
!        allocate(yy(2880))
!        allocate(bb(2880))
!        read(1) xx
!        read(2) yy
!        read(3) bb
!        close(1)
!        close(2)
!        close(3)
        if (all(abs(x - xx) < .01)) then
            print *, 'x is equal'
        end if
        if (all(abs(y - yy) < .01)) then
            print *, 'y is equal'
        end if
        if (all(abs(b - bb) < .01)) then
            print *, 'b is equal'
        end if
        do i=1, size(bb)
            print *, b(i), bb(i)
        end do


  end subroutine test_bathy
    subroutine create_grid(X_mesh, Y_mesh, B_mesh, x, y, b, XXM, YYM, BBM)
        real(kind=8), allocatable, intent(inout), dimension(:,:) :: X_mesh, Y_mesh, B_mesh, XXM, YYM, BBM
        real(kind=8), dimension(:), intent(inout) :: x, y, b
        real(kind=8) :: xll, yll, bll
        integer :: i,j
        ! fill x and y matrices a la np.meshgrid
        allocate(X_mesh(size(x), size(y)))
        allocate(Y_mesh(size(x), size(y)))
        allocate(B_mesh(size(b), size(y)))
        allocate(XXM(1-mbc:mx+mbc,1-mbc:my+mbc))
        allocate(YYM(1-mbc:mx+mbc,1-mbc:my+mbc))
        allocate(BBM(1-mbc:mx+mbc,1-mbc:my+mbc))
!        print *, shape(X_mesh), shape(Y_mesh), shape(B_mesh)
!        do i=1, size(y)
!            do j=1, size(x)
!                X_mesh(i,j) = x(j)
!                Y_mesh(i,j) = y(i)
!                B_mesh(i,j) = b(i)
!            end do
!        end do
        X_mesh = spread(x, 2, size(y))
        Y_mesh = spread(y, 1, size(x))
        B_mesh = spread(b, 1, size(x))
!        print *, X_mesh
        do j=1-mbc,my+mbc
            yll = ylower + (j-0.5d0) * dy
            do i=1-mbc,mx+mbc
                xll = xlower + (i-0.5d0) * dx
                bll = depth + (j-0.5d0)*db
                ! Location logic
                !            aux(1, i, j) = something
                XXM(i,j) = xll
                YYM(i,j) = yll
                BBM(i,j) = bll
            end do
        end do
    end subroutine create_grid
    subroutine test_grid(X_mesh, Y_mesh, B_mesh, XXM, YYM, BBM)
        real(kind=8), intent(in), dimension(:,:) :: X_mesh, Y_mesh, B_mesh
        real(kind=8), intent(in), dimension(:,:) :: XXM, YYM, BBM
        integer :: i,j
!        open(1, File='X_grid.txt', form='unformatted')
!        open(2, File='Y_grid.txt', form='unformatted')
!        open(3, File='B_grid.txt', form='unformatted')
!        read(1) xx_mesh
!        read(2) yy_mesh
!        read(3) bb_mesh
!        close(1)
!        close(2)
!        close(3)
        print *, shape(B_mesh), shape(Y_mesh), shape(X_mesh)
!        print *, B_mesh
        if (all(abs(X_mesh - XXM) < .01)) then
            print *, 'X is equal'
        end if
        if (all(abs(Y_mesh - YYM) < .01)) then
            print *, 'Y is equal'
        end if
        if (all(abs(B_mesh - BBM) < .01)) then
            print *, 'B is equal'
        end if
!        do j =1, size(XXM,2)
!            do i = 1, size(XXM,1)
!                print *, B_mesh(i,j), BBM(i,j)
!            end do
!        end do
        end subroutine test_grid
    subroutine create_island(B_mesh, Y_mesh, bathy)
        real(kind=8), intent(in), dimension(:,:) :: Y_mesh, B_mesh
        real(kind=8), allocatable, dimension(:,:), intent(inout) :: bathy
        real :: isle_loc, isle_width, slope, base, isle_start, isle_end, isle_height
        integer :: i, j
        allocate(bathy(size(B_mesh, 1), size(B_mesh, 2)))
        isle_loc = 25.6
        isle_width = 0.2
        slope = 500/600e3
        base = isle_width / cos(slope)
        isle_start = isle_loc - (base/2)
        isle_end = isle_loc + (base/2)
        isle_height = 2
        do i = 1, size(B_mesh, 1)
            do j = 1, size(B_mesh, 2)
                if (Y_mesh(i, j) < isle_start) then
!                    print *, 'no island yet'
                    bathy(i,j) = B_mesh(i, j)
                    elseif (Y_mesh(i, j) >= isle_start .and. Y_mesh(i, j) <= isle_end) then
!                        print *, i, j
                    bathy(i,j) = isle_height
!                    print *, 'island', bathy(i,j)
                    elseif (Y_mesh(i,j) > isle_end) then
                        bathy(i,j) = B_mesh(i,j)

                end if
            end do
        end do


    end subroutine create_island
    subroutine test_island(bathy)
        real(kind=8),  dimension(:,:), intent(in) :: bathy
        real, dimension(2880,3480) :: in_bathy

        open(1, File='Bathy.txt', form='unformatted')
        read(1) in_bathy
        close(1)
!        print *, bathy
        if (all(abs(bathy - in_bathy) < .01)) then
            print *, 'Bathy is equal'
        end if

    end subroutine test_island

    subroutine create_breach(X_mesh, Y_mesh, bathy, t)
        real(kind=8), intent(in), dimension(:,:) :: X_mesh, Y_mesh, bathy
        real(kind=8), intent(in) :: t
        integer :: rowidx, colidx
        real(kind=8) :: sigma, x1, x2, y1, y2, xcol, ycol, mu, amp, t1
        ! Add breach parameters
        x1 = -88.0 ! left side of breach
        x2 = -86.0 ! right side of breach
        mu = -87.0 ! center of breach (expected value)
        y1 = 25.5 ! bottom of breach
        y2 = 25.7 ! top of breach
        sigma = 1.0 ! variance

        allocate(breach(size(bathy, 1), size(bathy, 2)))
        t1 = -200000.0
        if (t<t1) then
            amp =0.0
        elseif (t>t1) then
            amp=10.0
        end if
        ! Breach the barrier island depending on time
        breach = bathy
        do rowidx = 1, size(X_mesh, 1)
            do colidx = 1, size(X_mesh, 2)
                xcol = X_mesh(rowidx, colidx)
                ycol = Y_mesh(rowidx, colidx)
                if ((xcol >= x1) .and. (xcol <= x2) .and. &
                        ( ycol >= y1) .and. (ycol <= y2)) then
                    breach(rowidx, colidx) = breach(rowidx, colidx) &
                            - (10.0 * exp(-0.5 * (X_mesh(rowidx, colidx) - mu)**2/(sigma**2)) * 0.55*breach(rowidx, colidx))
!                    if(breach(rowidx, colidx)< 0) then
!                        breach(rowidx, colidx) = 0

!                    end if
                end if
            end do
        end do

    end subroutine create_breach
    subroutine test_breach(breach)
        real(kind=8),  dimension(:,:), intent(in) :: breach
        real, dimension(2880,3480) :: py_breach

        open(1, File='breach.txt', form='unformatted')
        read(1) py_breach
        close(1)
        if (all(abs(breach - py_breach) < .01)) then
            print *, 'Breach is equal'
        end if

    end subroutine test_breach

end program barrier_breach
