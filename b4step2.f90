! ============================================
subroutine b4step2(mbc,mx,my,meqn,q,xlower,ylower,dx,dy,t,dt,maux,aux)
! ============================================
!
! # called before each call to step
! # use to set time-dependent aux arrays or perform other tasks.
!
! This particular routine sets negative values of q(1,i,j) to zero,
! as well as the corresponding q(m,i,j) for m=1,meqn.
! This is for problems where q(1,i,j) is a depth.
! This should occur only because of rounding error.
!
! Also calls movetopo if topography might be moving.

    use geoclaw_module, only: dry_tolerance
    use geoclaw_module, only: g => grav
    use topo_module, only: num_dtopo,topotime
    use topo_module, only: aux_finalized
    use topo_module, only: xlowdtopo,xhidtopo,ylowdtopo,yhidtopo

    use amr_module, only: xlowdomain => xlower
    use amr_module, only: ylowdomain => ylower
    use amr_module, only: xhidomain => xupper
    use amr_module, only: yhidomain => yupper
    use amr_module, only: xperdom,yperdom,spheredom,NEEDS_TO_BE_SET

    use storm_module, only: set_storm_fields
    implicit none

    ! Subroutine arguments
    integer, intent(in) :: meqn
    integer, intent(inout) :: mbc,mx,my,maux
    real(kind=8), intent(inout) :: xlower, ylower, dx, dy, t, dt
    real(kind=8), intent(inout) :: q(meqn,1-mbc:mx+mbc,1-mbc:my+mbc)
    real(kind=8), intent(inout) :: aux(maux,1-mbc:mx+mbc,1-mbc:my+mbc)


    ! Local storage
    integer :: index,i,j,k,dummy
    real(kind=8) :: h,u,v
    CHARACTER(len=52), PARAMETER :: file_path = "/groups/weiszr_lab/catherine/breach_sim/b4step_mesh/"
    CHARACTER(len=10) :: xll, yll
    CHARACTER(len=25) :: file_name


    ! Check for NaNs in the solution
    call check4nans(meqn,mbc,mx,my,q,t,1)

    ! check for h < 0 and reset to zero
    ! check for h < drytolerance
    ! set hu = hv = 0 in all these cells
    forall(i=1-mbc:mx+mbc, j=1-mbc:my+mbc,q(1,i,j) < dry_tolerance)
        q(1,i,j) = max(q(1,i,j),0.d0)
        q(2:3,i,j) = 0.d0
    end forall
!    write(xll, '(f5.2)') abs(xlower)
!    write(yll, '(f5.2)') abs(ylower)
!    write(file_name, '(a,a,a,a)') trim(xll), '_', trim(yll),'.dat'
!    open(unit=9, file=file_path//file_name )
!    write(9, *) xlower
!    write(9, *) ylower
!    write(9, *) dx
!    write(9, *) dy
!    write(9, *) mx
!    write(9, *) my
!    close(9)
    if (aux_finalized < 2) then
        print *, 'RESETTING AUX'
        ! topo arrays might have been updated by dtopo more recently than
        ! aux arrays were set unless at least 1 step taken on all levels
        aux(1,:,:) = NEEDS_TO_BE_SET ! new system checks this val before setting
        call setaux(mbc,mx,my,xlower,ylower,dx,dy,maux,aux)
    endif

    ! !!!!!Change xlower and ylower compare values to varialbes read from file

   if ((xlower > -88.0) .and. (xlower < -86.0) .and. &
        (ylower < 26.0) .and. (ylower > 25.0)) then

           print *, 'Gonna call barrier breach!'
           call barrier_breach(maux,mbc,mx,my,xlower,ylower,dx,dy,t,dt,aux)

   end if

    ! Set wind and pressure aux variables for this grid
    call set_storm_fields(maux,mbc,mx,my,xlower,ylower,dx,dy,t,aux)

end subroutine b4step2

subroutine barrier_breach(maux,mbc,mx,my,xlower,ylower,dx,dy,t,dt,aux)
implicit none
! Allocate variables
! Subroutine variables
integer, intent(inout) :: mbc,mx,my,maux
real(kind=8), intent(inout) :: xlower, ylower, dx, dy, t, dt
real(kind=8), intent(inout) :: aux(maux,1-mbc:mx+mbc,1-mbc:my+mbc)

! Local variables
real(kind=8), allocatable, dimension(:) :: x, y, b
real(kind=8), allocatable, dimension(:,:) :: X_mesh, Y_mesh, B_mesh, breach
real(kind=8) :: bathy(1-mbc:mx+mbc,1-mbc:my+mbc)
real(kind=8) :: db,depth
integer :: i,j

CHARACTER(len=52), PARAMETER :: fileplace = "/groups/weiszr_lab/catherine/breach_sim/breach_mesh/"
CHARACTER(len=10) :: xll, yll
CHARACTER(len=25) :: file_name

!write(xll, '(f5.2)') abs(xlower)
!write(yll, '(f5.2)') abs(ylower)
!write(file_name, '(a,a,a,a)') trim(xll), '_', trim(yll),'.dat'
!
!open(unit=11, file=fileplace//file_name)
!write(11, *) xlower
!write(11, *) ylower
!write(11, *) dx
!write(11, *) dy
!write(11, *) mx
!write(11, *) my
!close(11)

depth = minval(aux(1,:,:))
db = 1.73 ! value from original bathymetry
!print *, 'AUX', aux(1,:,:)
call create_bathy(xlower, ylower, mx, my, x, y, dx, dy, b, db, depth, mbc)
call create_grid(X_mesh, Y_mesh, B_mesh, x, y, b)

! edit this to make it generic for small patches
!call create_island(B_mesh, Y_mesh, bathy)
!allocate(bathy(size(B_mesh, 1), size(B_mesh, 2)))
!call test_aux1(x, y, b, X_mesh, Y_mesh, B_mesh, bathy, depth, dx, dy, db, mx, my, xlower, ylower, aux)
do j=1-mbc,my+mbc

    do i=1-mbc,mx+mbc

        bathy(i,j) = aux(1,i,j)


        end do
        end do
call create_breach(X_mesh, Y_mesh, bathy, t, aux)
!do j=1, size(breach, 2)
!
!    do i=1, size(breach, 1)
!
!        aux(1,i,j) = breach(i,j)


!    end do
!end do

contains
subroutine test_aux1(x, y, b, X_mesh, Y_mesh, B_mesh, bathy, depth, dx, dy, db, mx, my, xlower, ylower, aux)
    real(kind=8), allocatable, dimension(:), intent(inout) :: x, y, b
    real(kind=8), allocatable, dimension(:,:), intent(inout) :: X_mesh, Y_mesh, B_mesh, bathy
    real(kind=8), intent(inout) :: dx, dy, db, xlower, ylower, depth
    integer, intent(inout) :: mx, my
    real(kind=8), intent(inout), dimension(:,:,:) :: aux
    integer :: i, j
    ! create bathymetry from scratch
    call create_bathy(xlower, ylower, mx, my, x, y, dx, dy, b, db, depth, mbc)
    call create_grid(X_mesh, Y_mesh, B_mesh, x, y, b)

    ! edit this to make it generic for small patches
    call create_island(B_mesh, Y_mesh, bathy)
!    print *, 'Bathy', bathy
!    print *, 'Aux', aux(1,:,:)
!
!    if (all(abs(bathy - aux(1,:,:)) < 2.01)) then
!        print *, 'Bathy is equal'
!    else
!        do j=1, size(bathy, 2)
!            print *, 'i = ', i
!            do i = 1, size(bathy, 1)
!                print *, 'j =', j
!                print *, 'Bathy is not equal', bathy(i,j), aux(1,i,j)
!
!            end do
!        end do
!
!    end if

end subroutine test_aux1

subroutine create_bathy(xlower, ylower, mx, my, x, y, dx, dy, b, db, depth, mbc)
    implicit none
    ! Subroutine variables
    ! Subroutine variables imported from b4step2.f90
    integer, intent(inout) :: mx, my, mbc
    real(kind=8), intent(inout) :: xlower, ylower, dx, dy, db, depth
    real(kind=8), allocatable, dimension(:), intent(inout) :: x, y, b
    integer :: i
    ! fill x and y like np.linspace
    allocate(x(1-mbc:mx+mbc))
    allocate(y(1-mbc:my+mbc))
    allocate(b(1-mbc:my+mbc))
    x = (/((i-0.5d0)*dx + xlower, i=1-mbc,mx+mbc)/)
    y = (/((i-0.5d0)*dy + ylower, i=1-mbc,my+mbc)/)
    b = (/((i-0.5d0)*db + depth, i=1-mbc,my+mbc)/)
    !    print *, db, depth
    !     do i = 1, size(b)
    !       print *, b(i)
    !     end do
end subroutine create_bathy

subroutine create_grid(X_mesh, Y_mesh, B_mesh, x, y, b)
    real(kind=8), allocatable, intent(inout), dimension(:,:) :: X_mesh, Y_mesh, B_mesh
    real(kind=8), dimension(:), intent(inout) :: x, y, b
    real(kind=8) :: xll, yll, bll
    integer :: i,j
    ! fill x and y matrices a la np.meshgrid
    allocate(X_mesh(size(x), size(y)))
    allocate(Y_mesh(size(x), size(y)))
    allocate(B_mesh(size(b), size(y)))
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
end subroutine create_grid

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
    do j = 1, size(B_mesh, 2)
        do i = 1, size(B_mesh, 1)
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

subroutine create_breach(X_mesh, Y_mesh, bathy, t,  aux)
    real(kind=8), intent(in), dimension(1-mbc:,1-mbc:) :: X_mesh, Y_mesh, bathy
    real(kind=8), intent(in) :: t
!    real(kind=8), intent(inout), allocatable, dimension(:,:) :: breach
    real(kind=8), intent(inout) :: aux(maux,1-mbc:mx+mbc,1-mbc:my+mbc)
    integer :: rowidx, colidx, i, j
    real(kind=8) :: sigma, x, y, x1, x2, y1, y2, xcol, ycol, mu, amp, t1, island, height
    ! Add breach parameters
    x1 = -88.0 ! left side of breach
    x2 = -86.0 ! right side of breach
    mu = -87.0 ! center of breach (expected value)
    y1 = 25.5 ! bottom of breach
    y2 = 25.7 ! top of breach
    sigma = 1.0 ! variance
    height = 2.0
!    allocate(breach(size(bathy, 1), size(bathy, 2)))
    t1 = -200000.0
    if (t<t1) then
        amp =0.0
    elseif (t>t1) then
        amp=10.0
    end if
    print *, 'The patch size is: ', my, mx
    ! Breach the barrier island depending on time
!    breach(:,:) = bathy(:,:)


!    do j=1-mbc,my+mbc
!        y = ylower + (j-0.5d0) * dy     ! Degrees latitude
!        f = coriolis(y)
!        do i=1-mbc,mx+mbc
!            x = xlower + (i-0.5d0) * dx   ! Degrees longitude


    do j = 1-mbc,my+mbc
        y = ylower + (j-0.5d0) * dy
        do i = 1-mbc,mx+mbc
            x = xlower + (i-0.5d0) * dx
            island = aux(1, i, j)
            if ((x >= x1) .and. (x <= x2) .and. &
                    ( y >= y1) .and. (y <= y2) .and. &
                    (island > 0.0) .and. (island <= height)) then
!                print *, "Before breach", aux(1, rowidx, colidx), 'X', X_mesh(rowidx, colidx), 'Y', Y_mesh(rowidx,colidx)
                aux(1,i, j) = 10.0 !aux(1,i, j) - 2.00 ! &
!                        - (10.0 * exp(-0.5 * (X_mesh(i, j) - mu)**2/(sigma**2)) * 0.55*aux(1,i, j))
!!                print *, 'After breach', aux(1,rowidx, colidx)
!                    if (aux(1,i, j) < 0) then
!                        aux(1,i, j) = 0
!                    end if
            end if
        end do
    end do

end subroutine create_breach

end subroutine barrier_breach